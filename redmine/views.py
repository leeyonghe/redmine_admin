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
from .models import Project, Issue, TimeEntry, IssueStatus, Tracker, RedmineUser
from django.contrib.auth.models import User
# Create your views here.

@login_required
def index(request):
    print("index")
    # 실제 데이터 가져오기
    total_projects = Project.objects.count()
    total_issues = Issue.objects.count()
    completed_issues = Issue.objects.filter(status_id=5).count()  # 종료된 이슈
    active_users = TimeEntry.objects.values('user').distinct().count()
    print("index")
    
    # 최근 활동
    recent_issues = Issue.objects.select_related('project').order_by('-created_on')[:5]
    
    # 프로젝트별 통계
    project_stats = Project.objects.annotate(
        issue_count=Count('issue'),
        completed_count=Count('issue', filter=Q(issue__status_id=5))
    ).order_by('-issue_count')[:5]

    print("index")
    
    context = {
        'total_projects': total_projects,
        'total_issues': total_issues,
        'completed_issues': completed_issues,
        'active_users': active_users,
        'recent_issues': recent_issues,
        'project_stats': project_stats,
    }

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
            except RedmineUser.DoesNotExist:
                user_data['user_login'] = f"User_{user_data['assigned_to_id']}"
                user_data['user_firstname'] = "Unknown"
                user_data['user_lastname'] = "User"
        
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