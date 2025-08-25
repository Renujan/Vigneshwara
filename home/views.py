from django.http import JsonResponse
from django.utils import timezone
from django.db.models import Count
from django.contrib.auth.decorators import user_passes_test
from django.db.models.functions import ExtractMonth


from contact_details.models import Contact


from datetime import datetime, timedelta

def is_admin(user):
    return user.is_superuser

@user_passes_test(is_admin)
def dashboard_stats(request):
    entity_type = request.GET.get('entity_type', 'items')
    period = request.GET.get('period', 'month')
    
    totals = {
        'total_items': Items.objects.count(),
        'total_contacts': Contact.objects.count(),
        'total_enquiries': Enquire.objects.count(),
    }

    graph_data = {}
    
    model_map = {
        'items': Items,
        'contacts': Contact,
        'enquiries': Enquire,
    }
    
    model = model_map.get(entity_type)
    
    if not model:
        return JsonResponse({'error': 'Invalid entity type'}, status=400)

    # All models are assumed to have a 'created_at' field.
    date_field = 'created_at'

    if period == 'month':
        year = int(request.GET.get('year', timezone.now().year))
        labels = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        data = [0] * 12
        
        filter_kwargs = {f'{date_field}__year': year}
        # Exclude null dates to prevent errors and use database-level month extraction
        counts = model.objects.filter(**filter_kwargs).exclude(**{f'{date_field}__isnull': True}) \
            .annotate(month=ExtractMonth(date_field)) \
            .values('month') \
            .annotate(c=Count('id')) \
            .values('month', 'c')

        for count in counts:
            # month is 1-based, list index is 0-based
            if count['month'] is not None:
                data[count['month'] - 1] = count['c']
            
    elif period == 'year':
        labels = []
        data = []
        current_year = timezone.now().year
        for i in range(4, -1, -1):
            year = current_year - i
            labels.append(year)
            filter_kwargs = {f'{date_field}__year': year}
            count = model.objects.filter(**filter_kwargs).count()
            data.append(count)

    elif period == 'custom':
        start_date_str = request.GET.get('start_date')
        end_date_str = request.GET.get('end_date')
        aggregation = request.GET.get('aggregation', 'day')

        try:
            start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
            end_date = datetime.strptime(end_date_str, '%Y-%m-%d')
        except (ValueError, TypeError):
            return JsonResponse({'error': 'Invalid date format'}, status=400)

        labels = []
        data = []
        
        current_date = start_date
        while current_date <= end_date:
            if aggregation == 'day':
                labels.append(current_date.strftime('%b %d'))
                filter_kwargs = {f'{date_field}__date': current_date}
                count = model.objects.filter(**filter_kwargs).count()
                data.append(count)
                current_date += timedelta(days=1)
            elif aggregation == 'week':
                start_of_week = current_date - timedelta(days=current_date.weekday())
                end_of_week = start_of_week + timedelta(days=6)
                labels.append(f"Week of {start_of_week.strftime('%b %d')}")
                filter_kwargs = {f'{date_field}__date__range': [start_of_week, end_of_week]}
                count = model.objects.filter(**filter_kwargs).count()
                data.append(count)
                current_date += timedelta(weeks=1)
            elif aggregation == 'month':
                labels.append(current_date.strftime('%b %Y'))
                filter_kwargs = {f'{date_field}__year': current_date.year, f'{date_field}__month': current_date.month}
                count = model.objects.filter(**filter_kwargs).count()
                data.append(count)
                # Move to the first day of the next month
                if current_date.month == 12:
                    current_date = current_date.replace(year=current_date.year + 1, month=1, day=1)
                else:
                    current_date = current_date.replace(month=current_date.month + 1, day=1)
            else: # year
                labels.append(current_date.year)
                filter_kwargs = {f'{date_field}__year': current_date.year}
                count = model.objects.filter(**filter_kwargs).count()
                data.append(count)
                current_date = current_date.replace(year=current_date.year + 1, day=1)


    graph_data = {
        'labels': labels,
        'data_series': {
            'label': f'{entity_type.capitalize()} Trend',
            'data': data,
        },
        'entity_type': entity_type,
        'period': period,
    }

    response_data = {
        'totals': totals,
        'graph_data': graph_data,
    }
    
    return JsonResponse(response_data)
