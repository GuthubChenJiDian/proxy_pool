from concurrent.futures.process import ProcessPoolExecutor

import setting
from entity.proxy import Proxy
from fetcher.ProxyFetcher import ProxyFetcher
from validator.do_validator import DoValidator


conf = setting


def proxy_fetcher_process(fetch_source):
    fetcher = getattr(ProxyFetcher, fetch_source, None)
    if not fetcher:
        # self.log.error("ProxyFetch - {func}: class method not exists!".format(func=fetch_source))
        return
    if not callable(fetcher):
        # self.log.error("ProxyFetch - {func}: must be class method".format(func=fetch_source))
        return
    return set(fetcher())


if __name__ == '__main__':
    # proxy_list = set()
    # fetchers = conf.PROXY_FETCHER
    #
    # # 多线程获取代理信息
    # futures = []
    # with ProcessPoolExecutor(max_workers=None) as executor:
    #     for fetch_source in fetchers:
    #         # self.log.info("ProxyFetch - {func}: start".format(func=fetch_source))
    #         futures.append(executor.submit(proxy_fetcher_process, fetch_source))
    #     for future in futures:
    #         proxy_list = proxy_list.union(future.result())
    #
    # # proxy_list = set(ProxyFetcher.freeProxy_kuaidaili())
    # # 先暂存到本地文件中
    # with open(setting.PROXY_ITEM_FILE, mode='w', encoding='utf-8') as f:
    #     for proxy in proxy_list:
    #         f.write(f'{proxy}\n')

    #首次代理检测
    proxy_list = []
    with open(setting.PROXY_ITEM_FILE, encoding='utf-8') as f:
        for line, val in enumerate(f):
            ip_port = val.rstrip('\n')
            proxy = DoValidator.validator(Proxy(ip_port), "raw")
            proxy_list.append(proxy)

    # 后续的定时代理检测
    for proxy in proxy_list:
        proxy = DoValidator.validator(proxy, "use")

    # 按照延迟排序
    proxy_list = sorted(proxy_list, key=lambda proxy: proxy.speed)

    for proxy in proxy_list:
        print(proxy.to_json())