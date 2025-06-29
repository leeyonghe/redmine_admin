from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.db.models import Count, Sum, Avg, Q
from django.utils import timezone
from datetime import datetime, timedelta
from .models import Project, Issue, TimeEntry, IssueStatus, Tracker

# Create your views here.

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
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        remember = request.POST.get('remember')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            if not remember:
                request.session.set_expiry(0)  # 브라우저 종료시 세션 만료
            return redirect('redmine:index')
        else:
            return render(request, 'login.html', {
                'error_message': '사용자명 또는 비밀번호가 올바르지 않습니다.'
            })
    
    return render(request, 'login.html')

def performance_view(request):
    try:
        print("performance_view start")
        # 개인별 성과 데이터
        user_performance = TimeEntry.objects.values(
            'user__login', 'user__firstname', 'user__lastname'
        ).annotate(
            total_hours=Sum('hours'),
            total_issues=Count('issue', distinct=True),
            avg_hours_per_issue=Avg('hours')
        ).order_by('-total_hours')
        print("user_performance query completed")
        
        # 부서별 통계 (프로젝트별로 그룹화)
        project_performance = Project.objects.annotate(
            total_hours=Sum('timeentry__hours'),
            total_issues=Count('issue'),
            completed_issues=Count('issue', filter=Q(issue__status_id=5))
        ).order_by('-total_hours')
        print("project_performance query completed")
        
        # 전체 평균 시간 계산
        total_avg_hours = TimeEntry.objects.aggregate(avg_hours=Avg('hours'))['avg_hours'] or 0
        print("total_avg_hours calculated")
        
        context = {
            'user_performance': user_performance,
            'project_performance': project_performance,
            'total_users': user_performance.count(),
            'avg_performance': total_avg_hours,
        }
        print("context created")
        
        return render(request, 'performance.html', context)
    except Exception as e:
        print(f"Error in performance_view: {str(e)}")
        return HttpResponse(f"Error: {str(e)}")

def weekly_report_view(request):
    # 현재 주의 데이터
    now = timezone.now()
    start_of_week = now - timedelta(days=now.weekday())
    end_of_week = start_of_week + timedelta(days=6)
    
    # 주간 통계
    weekly_issues = Issue.objects.filter(
        created_on__gte=start_of_week,
        created_on__lte=end_of_week
    )
    
    weekly_time_entries = TimeEntry.objects.filter(
        spent_on__gte=start_of_week.date(),
        spent_on__lte=end_of_week.date()
    )
    
    # 프로젝트별 주간 작업
    project_weekly_work = Project.objects.annotate(
        weekly_issues=Count('issue', filter=Q(
            issue__created_on__gte=start_of_week,
            issue__created_on__lte=end_of_week
        )),
        weekly_hours=Sum('timeentry__hours', filter=Q(
            timeentry__spent_on__gte=start_of_week.date(),
            timeentry__spent_on__lte=end_of_week.date()
        ))
    ).filter(weekly_issues__gt=0).order_by('-weekly_issues')
    
    context = {
        'week_start': start_of_week,
        'week_end': end_of_week,
        'total_weekly_issues': weekly_issues.count(),
        'completed_weekly_issues': weekly_issues.filter(status_id=5).count(),
        'in_progress_issues': weekly_issues.filter(status_id=2).count(),
        'delayed_issues': weekly_issues.filter(due_date__lt=now.date(), status_id__in=[1,2]).count(),
        'total_weekly_hours': weekly_time_entries.aggregate(total=Sum('hours'))['total'] or 0,
        'project_weekly_work': project_weekly_work,
        'weekly_issues': weekly_issues.select_related('project').order_by('-created_on'),
    }
    
    return render(request, 'weekly_report.html', context)

def monthly_report_view(request):
    # 현재 달의 데이터
    now = timezone.now()
    start_of_month = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    if now.month == 12:
        end_of_month = now.replace(year=now.year + 1, month=1, day=1) - timedelta(days=1)
    else:
        end_of_month = now.replace(month=now.month + 1, day=1) - timedelta(days=1)
    
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
        'month_start': start_of_month,
        'month_end': end_of_month,
        'total_monthly_issues': monthly_issues.count(),
        'completed_monthly_issues': monthly_issues.filter(status_id=5).count(),
        'total_monthly_hours': monthly_time_entries.aggregate(total=Sum('hours'))['total'] or 0,
        'project_performance': project_performance,
        'last_month_issues': last_month_issues,
        'issue_growth': ((monthly_issues.count() - last_month_issues) / last_month_issues * 100) if last_month_issues > 0 else 0,
    }
    
    return render(request, 'monthly_report.html', context)

def yearly_report_view(request):
    # 현재 연도의 데이터
    now = timezone.now()
    start_of_year = now.replace(month=1, day=1, hour=0, minute=0, second=0, microsecond=0)
    end_of_year = now.replace(month=12, day=31, hour=23, minute=59, second=59, microsecond=999999)
    
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
        'year_start': start_of_year,
        'year_end': end_of_year,
        'total_yearly_issues': yearly_issues.count(),
        'completed_yearly_issues': yearly_issues.filter(status_id=5).count(),
        'total_yearly_hours': yearly_time_entries.aggregate(total=Sum('hours'))['total'] or 0,
        'monthly_trends': monthly_trends,
        'department_performance': department_performance,
        'last_year_issues': last_year_issues,
        'issue_growth': ((yearly_issues.count() - last_year_issues) / last_year_issues * 100) if last_year_issues > 0 else 0,
    }
    
    return render(request, 'yearly_report.html', context) 