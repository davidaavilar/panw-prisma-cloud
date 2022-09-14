from checkov.common.models.enums import CheckResult, CheckCategories
from checkov.cloudformation.checks.resource.base_resource_check import BaseResourceCheck

class WEB_ACL_ALB(BaseResourceCheck):

    def __init__(self):
        name = "WEB_ACL_ALB"
        id = "CKV_CUSTOM_AWS_4"
        supported_resources = ['AWS::WAFv2::WebACL']
        categories = [CheckCategories.ENCRYPTION]
        super().__init__(name=name, id=id, categories=categories, supported_resources=supported_resources)

    def scan_resource_conf(self, conf):

        if 'Properties' in conf.keys():
            if 'Scope' in conf['Properties'].keys():
                if conf['Properties']['Scope'] not in 'REGIONAL':
                    return CheckResult.FAILED
                else:
                    if 'DefaultAction' not in conf['Properties'].keys():
                        return CheckResult.FAILED
                    elif 'Block' not in conf['Properties']['DefaultAction'].keys():
                        return CheckResult.FAILED
                    elif 'Block' in conf['Properties']['DefaultAction'].keys() and '__startline__' not in conf['Properties']['DefaultAction']['Block'].keys():
                        return CheckResult.FAILED
                    else:
                        if (
                            'RateBasedRuleCount' not in str(conf['Properties']['Rules'])
                            or 
                            'CountImperva' not in str(conf['Properties']['Rules'])
                            or 
                            'CountHealthcheck' not in str(conf['Properties']['Rules'])
                        ):
                            return CheckResult.FAILED
                        else:
                            for rule in conf['Properties']['Rules']:
                                if rule['Name'] == 'RateBasedRuleCount':
                                    if (
                                        rule['Statement']['RateBasedStatement']['AggregateKeyType'] != 'FORWARDED_IP'
                                        or
                                        rule['Statement']['RateBasedStatement']['ForwardedIPConfig']['HeaderName'] != 'x-forwarded-for'
                                        or
                                        'Count' not in rule['Action']
                                    ):
                                        return CheckResult.FAILED
                                elif rule['Name'] == 'CountImperva' or rule['Name'] == 'CountHealthcheck':
                                    if (
                                        'Allow' not in rule['Action']
                                    ):
                                        return CheckResult.FAILED
                    return CheckResult.PASSED
            else:
                return CheckResult.FAILED

        return CheckResult.PASSED

check = WEB_ACL_ALB()