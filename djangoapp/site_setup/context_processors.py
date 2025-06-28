from django.db.models import Prefetch
from site_setup.models import SiteSetup, MenuLink 


def context_processor_example(request):
    return {
        'example': 'Veio do context processor (example)'
    }


def site_setup(request):
    setup = (
        SiteSetup.objects
        .prefetch_related(
            Prefetch(
                'menu',
                queryset=MenuLink.objects.order_by('id')
            )
        )
        .order_by('-id')
        .first()
    )
    return {'site_setup': setup}