from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Count, Sum, Avg, Q, Case, When, ExpressionWrapper, F, FloatField
from django.db.models.functions import Cast
from django.db.models import Value
from django.utils import timezone
from datetime import datetime, timedelta
import hashlib
from .models import Project, Issue, TimeEntry, IssueStatus, Tracker, RedmineUser, RedmineUserAvatar
from django.contrib.auth.models import User
from django.db import connection
from django.utils.translation import activate, get_language
from django.http import JsonResponse
from django.conf import settings
# Create your views here.

def set_language(request):
    """언어 변경 뷰"""
    if request.method == 'POST':
        language = request.POST.get('language')
        print(f"Setting language to: {language}")  # 디버깅용
        
        if language in [lang[0] for lang in settings.LANGUAGES]:
            # 세션에 언어 설정 저장
            request.session[settings.LANGUAGE_COOKIE_NAME] = language
            print(f"Language saved to session: {request.session[settings.LANGUAGE_COOKIE_NAME]}")  # 디버깅용
            
            # 쿠키에도 설정
            response = JsonResponse({'status': 'success'})
            response.set_cookie(settings.LANGUAGE_COOKIE_NAME, language)
            return response
    return JsonResponse({'status': 'error'})

def get_current_language(request):
    """현재 언어를 가져오는 헬퍼 함수"""
    # 세션에서 언어 가져오기
    session_language = request.session.get(settings.LANGUAGE_COOKIE_NAME)
    # 쿠키에서 언어 가져오기
    cookie_language = request.COOKIES.get(settings.LANGUAGE_COOKIE_NAME)
    # 현재 언어 결정
    current_language = session_language or cookie_language or settings.LANGUAGE_CODE
    print(f"Current language: {current_language}")  # 디버깅용
    return current_language

@login_required
def index(request):
    print("index")
    # 실제 데이터 가져오기
    total_projects = Project.objects.count()
    total_issues = Issue.objects.count()
    completed_issues = Issue.objects.filter(status_id=5).count()  # 종료된 이슈
    active_users = RedmineUser.objects.filter(status=1).count()
    
    # 증감률 계산
    # 지난 달 대비 프로젝트 증감률
    last_month = timezone.now() - timedelta(days=30)
    last_month_projects = Project.objects.filter(created_on__lt=last_month).count()
    project_growth_rate = ((total_projects - last_month_projects) / last_month_projects * 100) if last_month_projects > 0 else 0
    
    # 지난 주 대비 완료된 작업 증감률
    last_week = timezone.now() - timedelta(days=7)
    last_week_completed = Issue.objects.filter(status_id=5, closed_on__lt=last_week).count()
    current_week_completed = Issue.objects.filter(status_id=5, closed_on__gte=last_week).count()
    completed_growth_rate = ((current_week_completed - last_week_completed) / last_week_completed * 100) if last_week_completed > 0 else 0
    
    # 지난 주 대비 총 이슈 증감률
    last_week_total = Issue.objects.filter(created_on__lt=last_week).count()
    current_week_total = Issue.objects.filter(created_on__gte=last_week).count()
    total_issues_growth_rate = ((current_week_total - last_week_total) / last_week_total * 100) if last_week_total > 0 else 0
    
    # 지난 달 대비 활성 사용자 증감률
    last_month_users = RedmineUser.objects.filter(status=1, created_on__lt=last_month).count()
    user_growth_rate = ((active_users - last_month_users) / last_month_users * 100) if last_month_users > 0 else 0
    
    print("index")
    
    # 최근 활동
    recent_issues = Issue.objects.select_related('project').order_by('-created_on')[:5]
    
    # 프로젝트별 통계
    project_stats = Project.objects.annotate(
        issue_count=Count('issue'),
        completed_count=Count('issue', filter=Q(issue__status_id=5))
    ).order_by('-issue_count')[:5]

    print("index")
    
    # 현재 언어 가져오기
    current_language = get_current_language(request)
    
    context = {
        'total_projects': total_projects,
        'total_issues': total_issues,
        'completed_issues': completed_issues,
        'active_users': active_users,
        'recent_issues': recent_issues,
        'project_stats': project_stats,
        'LANGUAGE_CODE': current_language,  # 언어 정보 추가
        'project_growth_rate': round(project_growth_rate, 1),
        'completed_growth_rate': round(completed_growth_rate, 1),
        'total_issues_growth_rate': round(total_issues_growth_rate, 1),
        'user_growth_rate': round(user_growth_rate, 1),
    }

    print(f"Context LANGUAGE_CODE: {context['LANGUAGE_CODE']}")  # 디버깅용
    print("index")
    
    return render(request, 'dashboard.html', context)

def login_view(request):
    # 이미 로그인된 사용자는 메인 페이지로 리다이렉트
    if request.user.is_authenticated:
        return redirect('redmine:index')
        
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        remember = request.POST.get('remember')

        print(f"Username: {username}")
        print(f"Password: {password}")
        print(f"Remember: {remember}")
        
        # Django의 authenticate() 함수 사용 (커스텀 백엔드가 자동으로 사용됨)
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            print(f"Login Success: {user.username}")
            login(request, user)
            
            if not remember:
                request.session.set_expiry(0)  # 브라우저 종료시 세션 만료
            
            # RedmineUser의 마지막 로그인 시간 업데이트
            try:
                redmine_user = RedmineUser.objects.get(login=username)
                redmine_user.last_login_on = timezone.now()
                redmine_user.save()
            except RedmineUser.DoesNotExist:
                pass
            
            return redirect('redmine:index')
        else:
            return render(request, 'login.html', {
                'error_message': '사용자명 또는 비밀번호가 올바르지 않습니다.'
            })
    
    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('redmine:login')

@login_required
def performance_view(request):
    try:
        print("performance_view start")
        
        # 개인별 성과 데이터 - 직접 Issue 테이블 참조
        user_performance = Issue.objects.values(
            'assigned_to_id'
        ).annotate(
            total_issues=Count('id'),
            completed_issues=Count('id', filter=Q(status_id=5)),
            in_progress_issues=Count('id', filter=Q(status_id=2)),
            new_issues=Count('id', filter=Q(status_id=1)),
            avg_priority=Avg('priority_id'),
            delayed_issues=Count('id', filter=Q(due_date__lt=timezone.now().date(), status_id__in=[1,2]))
        ).filter(assigned_to_id__isnull=False).order_by('-total_issues')
        
        # 사용자 정보 추가
        for user_data in user_performance:
            try:
                redmine_user = RedmineUser.objects.get(id=user_data['assigned_to_id'])
                user_data['user_login'] = redmine_user.login
                user_data['user_firstname'] = redmine_user.firstname
                user_data['user_lastname'] = redmine_user.lastname
                
                # 아바타 정보 추가 (테이블이 존재하지 않을 수 있으므로 안전하게 처리)
                try:
                    # 테이블 존재 여부 확인
                    with connection.cursor() as cursor:
                        cursor.execute("SHOW TABLES LIKE 'users_avatar'")
                        table_exists = cursor.fetchone()
                    
                    if table_exists:
                        avatar = RedmineUserAvatar.objects.get(user_id=redmine_user.id)
                        user_data['avatar_path'] = avatar.avatar_path
                    else:
                        user_data['avatar_path'] = None
                except Exception:
                    user_data['avatar_path'] = None
                    
            except RedmineUser.DoesNotExist:
                user_data['user_login'] = f"User_{user_data['assigned_to_id']}"
                user_data['user_firstname'] = "Unknown"
                user_data['user_lastname'] = "User"
                user_data['avatar_path'] = None
        
        print("user_performance query completed")
        
        # 프로젝트별 성과 - 직접 Issue 테이블 참조
        project_performance = Project.objects.annotate(
            total_issues=Count('issue'),
            completed_issues=Count('issue', filter=Q(issue__status_id=5)),
            in_progress_issues=Count('issue', filter=Q(issue__status_id=2)),
            new_issues=Count('issue', filter=Q(issue__status_id=1)),
            delayed_issues=Count('issue', filter=Q(issue__due_date__lt=timezone.now().date(), issue__status_id__in=[1,2])),
            avg_priority=Avg('issue__priority_id'),
            completion_rate=Case(
                When(total_issues=0, then=Value(0.0, output_field=FloatField())),
                default=ExpressionWrapper(
                    Cast('completed_issues', FloatField()) * 100.0 / Cast('total_issues', FloatField()),
                    output_field=FloatField()
                )
            )
        ).filter(total_issues__gt=0).order_by('-total_issues')
        
        print("project_performance query completed")
        
        # 전체 이슈 통계
        total_issues = Issue.objects.count()
        completed_issues = Issue.objects.filter(status_id=5).count()
        in_progress_issues = Issue.objects.filter(status_id=2).count()
        new_issues = Issue.objects.filter(status_id=1).count()
        delayed_issues = Issue.objects.filter(due_date__lt=timezone.now().date(), status_id__in=[1,2]).count()
        
        # 우선순위별 통계
        priority_stats = Issue.objects.values('priority_id').annotate(
            count=Count('id')
        ).order_by('priority_id')
        
        # 상태별 통계
        status_stats = Issue.objects.values('status_id').annotate(
            count=Count('id')
        ).order_by('status_id')
        
        print("total_avg_hours calculated")
        
        context = {
            'user_performance': user_performance,
            'project_performance': project_performance,
            'total_users': user_performance.count(),
            'total_issues': total_issues,
            'completed_issues': completed_issues,
            'in_progress_issues': in_progress_issues,
            'new_issues': new_issues,
            'delayed_issues': delayed_issues,
            'priority_stats': priority_stats,
            'status_stats': status_stats,
        }
        print("context created")
        
        return render(request, 'performance.html', context)
    except Exception as e:
        print(f"Error in performance_view: {str(e)}")
        return HttpResponse(f"Error: {str(e)}")

@login_required
def project_management_view(request):
    try:
        print("project_management_view start")
        
        # 프로젝트 통계
        total_projects = Project.objects.count()
        active_projects = Project.objects.filter(status=1).count()  # 활성 프로젝트
        delayed_projects = Project.objects.filter(
            Q(created_on__lt=timezone.now() - timedelta(days=30)) &  # 30일 이상 된 프로젝트
            Q(status=1)  # 아직 활성 상태
        ).count()
        total_team_members = RedmineUser.objects.filter(status=1).count()
        
        # 프로젝트 목록 (샘플 데이터)
        projects = []
        for project in Project.objects.all()[:10]:  # 최대 10개 프로젝트
            # 프로젝트별 이슈 통계
            project_issues = Issue.objects.filter(project=project)
            total_issues = project_issues.count()
            completed_issues = project_issues.filter(status_id=5).count()
            
            # 진행률 계산
            progress = 0
            if total_issues > 0:
                progress = round((completed_issues / total_issues) * 100)
            
            # 프로젝트 상태 결정
            if progress >= 100:
                status = 'completed'
            elif progress >= 50:
                status = 'active'
            elif project.created_on < timezone.now() - timedelta(days=30):
                status = 'delayed'
            else:
                status = 'waiting'
            
            # 담당자 정보 (첫 번째 이슈의 담당자)
            manager = "미지정"
            first_issue = project_issues.filter(assigned_to_id__isnull=False).first()
            if first_issue:
                try:
                    redmine_user = RedmineUser.objects.get(id=first_issue.assigned_to_id)
                    manager = f"{redmine_user.firstname} {redmine_user.lastname}"
                except RedmineUser.DoesNotExist:
                    pass
            
            projects.append({
                'id': project.id,
                'name': project.name,
                'description': project.description or "설명 없음",
                'status': status,
                'progress': progress,
                'manager': manager,
                'due_date': project.created_on + timedelta(days=90),  # 샘플 마감일
                'total_issues': total_issues,
                'completed_issues': completed_issues
            })
        
        context = {
            'total_projects': total_projects,
            'active_projects': active_projects,
            'delayed_projects': delayed_projects,
            'total_team_members': total_team_members,
            'projects': projects,
        }
        
        return render(request, 'project_management.html', context)
        
    except Exception as e:
        print(f"Error in project_management_view: {e}")
        context = {
            'total_projects': 0,
            'active_projects': 0,
            'delayed_projects': 0,
            'total_team_members': 0,
            'projects': [],
        }
        return render(request, 'project_management.html', context)

@login_required
def weekly_report_view(request, year=None, week=None):
    # 주차 파라미터가 없으면 현재 주 사용
    if year is None or week is None:
        now = timezone.now()
        year = now.year
        week = now.isocalendar()[1]  # ISO 주차
    
    # 해당 연도의 1월 1일
    year_start = datetime(year, 1, 1)
    
    # 해당 주의 시작일 계산 (월요일 기준)
    week_start = year_start + timedelta(days=(week - 1) * 7 - year_start.weekday())
    week_end = week_start + timedelta(days=6)
    
    # 이전 주와 다음 주 계산
    prev_week_start = week_start - timedelta(days=7)
    next_week_start = week_start + timedelta(days=7)
    
    prev_year, prev_week, _ = prev_week_start.isocalendar()
    next_year, next_week, _ = next_week_start.isocalendar()
    
    # 주간 통계
    weekly_issues = Issue.objects.filter(
        created_on__gte=week_start,
        created_on__lte=week_end
    ).select_related('project')

    weekly_issues = weekly_issues.select_related('project').order_by('-created_on')
    
    # 담당자 정보 추가
    for issue in weekly_issues:
        if issue.assigned_to_id:
            try:
                assigned_user = RedmineUser.objects.get(id=issue.assigned_to_id)
                issue.assigned_name = f"{assigned_user.firstname} {assigned_user.lastname}"
                print(f"assigned_name: {issue.assigned_name}")  
            except RedmineUser.DoesNotExist:
                issue.assigned_name = f"User_{issue.assigned_to_id}"
        else:
            issue.assigned_name = "미지정"
    
    # 멤버별 이슈 상태 통계 계산
    member_stats = {}
    for issue in weekly_issues:
        member_name = issue.assigned_name
        if member_name not in member_stats:
            member_stats[member_name] = {
                'total': 0,
                'new': 0,
                'in_progress': 0,
                'resolved': 0,
                'feedback': 0,
                'closed': 0,
                'rejected': 0
            }
        
        member_stats[member_name]['total'] += 1
        
        if issue.status_id == 1:
            member_stats[member_name]['new'] += 1
        elif issue.status_id == 2:
            member_stats[member_name]['in_progress'] += 1
        elif issue.status_id == 3:
            member_stats[member_name]['resolved'] += 1
        elif issue.status_id == 4:
            member_stats[member_name]['feedback'] += 1
        elif issue.status_id == 5:
            member_stats[member_name]['closed'] += 1
        elif issue.status_id == 6:
            member_stats[member_name]['rejected'] += 1
    
    weekly_time_entries = TimeEntry.objects.filter(
        spent_on__gte=week_start.date(),
        spent_on__lte=week_end.date()
    )
    
    # 프로젝트별 주간 작업
    project_weekly_work = Project.objects.annotate(
        weekly_issues=Count('issue', filter=Q(
            issue__created_on__gte=week_start,
            issue__created_on__lte=week_end
        )),
        weekly_hours=Sum('timeentry__hours', filter=Q(
            timeentry__spent_on__gte=week_start.date(),
            timeentry__spent_on__lte=week_end.date()
        ))
    ).filter(weekly_issues__gt=0).order_by('-weekly_issues')
    
    context = {
        'year': year,
        'week': week,
        'week_start': week_start,
        'week_end': week_end,
        'prev_year': prev_year,
        'prev_week': prev_week,
        'next_year': next_year,
        'next_week': next_week,
        'total_weekly_issues': weekly_issues.count(),
        'completed_weekly_issues': weekly_issues.filter(status_id=5).count(),
        'in_progress_issues': weekly_issues.filter(status_id=2).count(),
        'delayed_issues': weekly_issues.filter(due_date__lt=timezone.now().date(), status_id__in=[1,2]).count(),
        'total_weekly_hours': weekly_time_entries.aggregate(total=Sum('hours'))['total'] or 0,
        'project_weekly_work': project_weekly_work,
        'weekly_issues': weekly_issues,
        'member_stats': member_stats,
    }
    
    return render(request, 'weekly_report.html', context)

@login_required
def monthly_report_view(request, year=None, month=None):
    # 월 파라미터가 없으면 현재 월 사용
    if year is None or month is None:
        now = timezone.now()
        year = now.year
        month = now.month
    
    # 해당 월의 시작일과 종료일 계산
    start_of_month = datetime(year, month, 1)
    if month == 12:
        end_of_month = datetime(year + 1, 1, 1) - timedelta(days=1)
    else:
        end_of_month = datetime(year, month + 1, 1) - timedelta(days=1)
    
    # 이전 월과 다음 월 계산
    if month == 1:
        prev_month = 12
        prev_year = year - 1
    else:
        prev_month = month - 1
        prev_year = year
    
    if month == 12:
        next_month = 1
        next_year = year + 1
    else:
        next_month = month + 1
        next_year = year
    
    # 월간 통계
    monthly_issues = Issue.objects.filter(
        created_on__gte=start_of_month,
        created_on__lte=end_of_month
    )
    
    monthly_time_entries = TimeEntry.objects.filter(
        spent_on__gte=start_of_month.date(),
        spent_on__lte=end_of_month.date()
    )
    
    # 프로젝트별 성과
    project_performance = Project.objects.annotate(
        monthly_issues=Count('issue', filter=Q(
            issue__created_on__gte=start_of_month,
            issue__created_on__lte=end_of_month
        )),
        monthly_hours=Sum('timeentry__hours', filter=Q(
            timeentry__spent_on__gte=start_of_month.date(),
            timeentry__spent_on__lte=end_of_month.date()
        )),
        completed_issues=Count('issue', filter=Q(
            issue__created_on__gte=start_of_month,
            issue__created_on__lte=end_of_month,
            issue__status_id=5
        ))
    ).filter(monthly_issues__gt=0).order_by('-monthly_issues')
    
    # 전월 대비 비교
    last_month_start = start_of_month - timedelta(days=30)
    last_month_issues = Issue.objects.filter(
        created_on__gte=last_month_start,
        created_on__lt=start_of_month
    ).count()
    
    context = {
        'year': year,
        'month': month,
        'month_start': start_of_month,
        'month_end': end_of_month,
        'prev_year': prev_year,
        'prev_month': prev_month,
        'next_year': next_year,
        'next_month': next_month,
        'total_monthly_issues': monthly_issues.count(),
        'completed_monthly_issues': monthly_issues.filter(status_id=5).count(),
        'total_monthly_hours': monthly_time_entries.aggregate(total=Sum('hours'))['total'] or 0,
        'project_performance': project_performance,
        'last_month_issues': last_month_issues,
        'issue_growth': ((monthly_issues.count() - last_month_issues) / last_month_issues * 100) if last_month_issues > 0 else 0,
    }
    
    return render(request, 'monthly_report.html', context)

@login_required
def yearly_report_view(request, year=None):
    # 연도 파라미터가 없으면 현재 연도 사용
    if year is None:
        now = timezone.now()
        year = now.year
    
    # 해당 연도의 시작일과 종료일 계산
    start_of_year = datetime(year, 1, 1)
    end_of_year = datetime(year, 12, 31, 23, 59, 59, 999999)
    
    # 이전 연도와 다음 연도 계산
    prev_year = year - 1
    next_year = year + 1
    
    # 연간 통계
    yearly_issues = Issue.objects.filter(
        created_on__gte=start_of_year,
        created_on__lte=end_of_year
    )
    
    yearly_time_entries = TimeEntry.objects.filter(
        spent_on__gte=start_of_year.date(),
        spent_on__lte=end_of_year.date()
    )
    
    # 월별 트렌드
    monthly_trends = []
    for month in range(1, 13):
        month_start = start_of_year.replace(month=month)
        if month == 12:
            month_end = end_of_year
        else:
            month_end = start_of_year.replace(month=month + 1) - timedelta(days=1)
        
        month_issues = Issue.objects.filter(
            created_on__gte=month_start,
            created_on__lte=month_end
        ).count()
        
        monthly_trends.append({
            'month': month,
            'issues': month_issues,
            'percentage': (month_issues / yearly_issues.count() * 100) if yearly_issues.count() > 0 else 0
        })
    
    # 부서별 성과 (프로젝트별)
    department_performance = Project.objects.annotate(
        yearly_issues=Count('issue', filter=Q(
            issue__created_on__gte=start_of_year,
            issue__created_on__lte=end_of_year
        )),
        yearly_hours=Sum('timeentry__hours', filter=Q(
            timeentry__spent_on__gte=start_of_year.date(),
            timeentry__spent_on__lte=end_of_year.date()
        )),
        completed_issues=Count('issue', filter=Q(
            issue__created_on__gte=start_of_year,
            issue__created_on__lte=end_of_year,
            issue__status_id=5
        ))
    ).filter(yearly_issues__gt=0).order_by('-yearly_issues')
    
    # 전년 대비 비교
    last_year_start = start_of_year - timedelta(days=365)
    last_year_issues = Issue.objects.filter(
        created_on__gte=last_year_start,
        created_on__lt=start_of_year
    ).count()
    
    context = {
        'year': year,
        'year_start': start_of_year,
        'year_end': end_of_year,
        'prev_year': prev_year,
        'next_year': next_year,
        'total_yearly_issues': yearly_issues.count(),
        'completed_yearly_issues': yearly_issues.filter(status_id=5).count(),
        'total_yearly_hours': yearly_time_entries.aggregate(total=Sum('hours'))['total'] or 0,
        'monthly_trends': monthly_trends,
        'department_performance': department_performance,
        'last_year_issues': last_year_issues,
        'issue_growth': ((yearly_issues.count() - last_year_issues) / last_year_issues * 100) if last_year_issues > 0 else 0,
    }
    
    return render(request, 'yearly_report.html', context)

def get_user_avatar_path(user_id):
    """사용자 ID로 아바타 경로를 가져오는 헬퍼 함수"""
    try:
        # 테이블 존재 여부 확인
        with connection.cursor() as cursor:
            cursor.execute("SHOW TABLES LIKE 'users_avatar'")
            table_exists = cursor.fetchone()
        
        if table_exists:
            avatar = RedmineUserAvatar.objects.get(user_id=user_id)
            return avatar.avatar_path
        else:
            return None
    except Exception:
        return None

@login_required
def get_user_detail(request, user_id):
    """사용자 상세 정보를 AJAX로 반환"""
    try:
        # 사용자 정보 가져오기
        redmine_user = RedmineUser.objects.get(id=user_id)
        
        # 사용자의 이슈 통계
        user_issues = Issue.objects.filter(assigned_to_id=user_id)
        total_issues = user_issues.count()
        completed_issues = user_issues.filter(status_id=5).count()
        in_progress_issues = user_issues.filter(status_id=2).count()
        new_issues = user_issues.filter(status_id=1).count()
        delayed_issues = user_issues.filter(due_date__lt=timezone.now().date(), status_id__in=[1,2]).count()
        
        # 최근 이슈 5개 - status_id를 사용하여 조인
        recent_issues = user_issues.select_related('project').order_by('-created_on')[:5]
        
        # 프로젝트별 이슈 분포
        project_distribution = user_issues.values('project__name').annotate(
            count=Count('id')
        ).order_by('-count')[:5]
        
        # 월별 완료 이슈 통계 (최근 6개월)
        six_months_ago = timezone.now() - timedelta(days=180)
        monthly_completed = user_issues.filter(
            status_id=5,
            closed_on__gte=six_months_ago
        ).extra(
            select={'month': "DATE_FORMAT(closed_on, '%%Y-%%m')"}
        ).values('month').annotate(
            count=Count('id')
        ).order_by('month')
        
        # 아바타 경로
        avatar_path = None
        try:
            with connection.cursor() as cursor:
                cursor.execute("SHOW TABLES LIKE 'users_avatar'")
                table_exists = cursor.fetchone()
            
            if table_exists:
                avatar = RedmineUserAvatar.objects.get(user_id=user_id)
                avatar_path = avatar.avatar_path
        except Exception:
            pass
        
        # 최근 이슈 데이터 준비 (status_id를 기반으로 상태명 매핑)
        status_names = {
            1: '신규',
            2: '진행중', 
            3: '해결됨',
            4: '피드백',
            5: '종료',
            6: '거부됨'
        }
        
        recent_issues_data = []
        for issue in recent_issues:
            recent_issues_data.append({
                'id': issue.id,
                'subject': issue.subject,
                'project__name': issue.project.name,
                'status__name': status_names.get(issue.status_id, '기타'),
                'priority_id': issue.priority_id,
                'created_on': issue.created_on.isoformat() if issue.created_on else None
            })
        
        context = {
            'user': {
                'id': redmine_user.id,
                'login': redmine_user.login,
                'firstname': redmine_user.firstname,
                'lastname': redmine_user.lastname,
                # 'email': redmine_user.mail,
                'created_on': redmine_user.created_on,
                'last_login_on': redmine_user.last_login_on,
                'avatar_path': avatar_path,
            },
            'stats': {
                'total_issues': total_issues,
                'completed_issues': completed_issues,
                'in_progress_issues': in_progress_issues,
                'new_issues': new_issues,
                'delayed_issues': delayed_issues,
                'completion_rate': round((completed_issues / total_issues * 100) if total_issues > 0 else 0, 1)
            },
            'recent_issues': recent_issues_data,
            'project_distribution': list(project_distribution),
            'monthly_completed': list(monthly_completed)
        }
        
        return JsonResponse(context)
        
    except RedmineUser.DoesNotExist:
        return JsonResponse({'error': '사용자를 찾을 수 없습니다.'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@login_required
def get_project_detail(request, project_id):
    """프로젝트 상세 정보를 JSON으로 반환"""
    try:
        # 프로젝트 정보 가져오기
        project = Project.objects.get(id=project_id)
        
        # 프로젝트 이슈 통계
        project_issues = Issue.objects.filter(project=project)
        total_issues = project_issues.count()
        completed_issues = project_issues.filter(status_id=5).count()
        in_progress_issues = project_issues.filter(status_id=2).count()
        new_issues = project_issues.filter(status_id=1).count()
        delayed_issues = project_issues.filter(
            due_date__lt=timezone.now().date(), 
            status_id__in=[1, 2]
        ).count()
        
        # 진행률 계산
        progress_rate = 0
        if total_issues > 0:
            progress_rate = round((completed_issues / total_issues) * 100)
        
        # 프로젝트 상태 결정
        if progress_rate >= 100:
            status = 'completed'
        elif progress_rate >= 50:
            status = 'active'
        elif project.created_on < timezone.now() - timedelta(days=30):
            status = 'delayed'
        else:
            status = 'waiting'
        
        # 담당자 정보 (첫 번째 이슈의 담당자)
        manager = "미지정"
        first_issue = project_issues.filter(assigned_to_id__isnull=False).first()
        if first_issue:
            try:
                redmine_user = RedmineUser.objects.get(id=first_issue.assigned_to_id)
                manager = f"{redmine_user.firstname} {redmine_user.lastname}"
            except RedmineUser.DoesNotExist:
                pass
        
        # 팀 멤버 정보 (프로젝트에 이슈가 할당된 사용자들)
        team_members = []
        assigned_users = project_issues.values('assigned_to_id').distinct()
        
        for user_data in assigned_users:
            if user_data['assigned_to_id']:
                try:
                    user = RedmineUser.objects.get(id=user_data['assigned_to_id'])
                    user_issues = project_issues.filter(assigned_to_id=user.id)
                    user_completed = user_issues.filter(status_id=5).count()
                    user_total = user_issues.count()
                    
                    team_members.append({
                        'id': user.id,
                        'name': f"{user.firstname} {user.lastname}",
                        'login': user.login,
                        # 'email': user.mail,
                        'role': '개발자',  # 기본 역할
                        'status': '활성',
                        'total_issues': user_total,
                        'completed_issues': user_completed,
                        'completion_rate': round((user_completed / user_total * 100) if user_total > 0 else 0, 1)
                    })
                except RedmineUser.DoesNotExist:
                    continue
        
        # 최근 이슈 (최근 5개)
        recent_issues = project_issues.order_by('-created_on')[:5]
        recent_issues_data = []
        
        # 상태명 매핑
        status_names = {
            1: '신규',
            2: '진행중', 
            3: '해결됨',
            4: '피드백',
            5: '종료',
            6: '거부됨'
        }
        
        for issue in recent_issues:
            # 담당자 정보 안전하게 처리
            assigned_to_name = '미지정'
            if issue.assigned_to_id:
                try:
                    assigned_user = RedmineUser.objects.get(id=issue.assigned_to_id)
                    assigned_to_name = f"{assigned_user.firstname} {assigned_user.lastname}"
                except RedmineUser.DoesNotExist:
                    pass
            
            recent_issues_data.append({
                'id': issue.id,
                'subject': issue.subject,
                'status': status_names.get(issue.status_id, 'Unknown'),
                'priority_id': issue.priority_id,
                'created_on': issue.created_on.strftime('%Y-%m-%d'),
                'assigned_to': assigned_to_name
            })
        
        # 프로젝트 정보
        project_data = {
            'id': project.id,
            'name': project.name,
            'description': project.description or "설명 없음",
            'status': status,
            'manager': manager,
            'created_on': project.created_on.strftime('%Y-%m-%d'),
            'due_date': (project.created_on + timedelta(days=90)).strftime('%Y-%m-%d'),  # 샘플 마감일
            'progress_rate': progress_rate
        }
        
        # 통계 정보
        stats = {
            'total_issues': total_issues,
            'completed_issues': completed_issues,
            'in_progress_issues': in_progress_issues,
            'new_issues': new_issues,
            'delayed_issues': delayed_issues,
            'progress_rate': progress_rate
        }
        
        return JsonResponse({
            'project': project_data,
            'stats': stats,
            'team_members': team_members,
            'recent_issues': recent_issues_data
        })
        
    except Project.DoesNotExist:
        return JsonResponse({'error': '프로젝트를 찾을 수 없습니다.'}, status=404)
    except Exception as e:
        print(f"Error in get_project_detail: {e}")
        return JsonResponse({'error': '프로젝트 정보를 가져오는 중 오류가 발생했습니다.'}, status=500) 