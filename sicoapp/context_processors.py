def user_groups_processor(request):
    return {
        'is_super_admin': request.user.groups.filter(name='superAdmin').exists(),
        'is_padmin': request.user.groups.filter(name='pAdministrator').exists(),
        'is_poperator': request.user.groups.filter(name='pOperator').exists(),
        'is_pregistrator': request.user.groups.filter(name='pRegistrator').exists(),
        'is_cadmin': request.user.groups.filter(name='cAdministrator').exists(),
        'is_coperator': request.user.groups.filter(name='cOperator').exists(),
    }