from urllib import request

class OutProcess(object):

    
    def __init__(self):
       pass
    def write_file(self, queue):
        try:
            while True:
                item = queue.get()
                if item:
                    
                    code, url = item.split('=')
                    print('code = %s, url = %s' % (code, url))
                    
                    if code == 'success':
                        with open('weixin_useable.txt', 'a') as fp:
                            fp.write(url + '\n')
                    elif code == 'pc_useable':                        
                        with open('pc_useable.txt', 'a') as fp:
                            fp.write(url + '\n')
                    else:
                        with open('disable.txt', 'a') as fp:
                            fp.write(url + '\n')
                    
        except Exception as e:
            print(e)