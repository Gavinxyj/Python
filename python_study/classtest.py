class Company(object):
    #提供一个快递服务接口
    def express_service(self, express_company):
         express_company.send()

#顺风快递公司
class FS(Company):
    def send(self):
        print('welcome to express by FS')

#中通跨地公司
class ZT(Company):
    def send(self):
        print('welcome to express by ZT')

#申通跨地公司
class ST(Company):
    def send(self):
        print('welcome to express by ST')

if __name__ == '__main__':
    service = Company()
    #使用FS快递服务
    fs = FS()
    service.express_service(fs)
    #使用ZT快递服务
    zt = ZT()
    service.express_service(zt)
    #使用ST快递服务
    st = ST()
    service.express_service(st)