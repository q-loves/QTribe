from django.conf import settings
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from itsdangerous import BadData


def generate_secret_openid(openid):
    """
    签名openid
    :param openid: 用户的openid
    :return: access_token
    """
    # 创建序列化器对象给数据加密
    serializer = Serializer(settings.SECRET_KEY,expires_in=600)
    data = {'openid': openid}
    token = serializer.dumps(data)
    return token.decode()

def check_secret_openid(sec_openid):
    """
    反解、反序列化access_token_openid
    :param access_token_openid: openid密文
    :return: openid明文
    """
    # 创建序列化器对象：序列化和反序列化的对象的参数必须是一模一样的
    s = Serializer(settings.SECRET_KEY, expires_in=600)
    print('sec_open---------->',sec_openid)

    # 反序列化openid密文
    try:
        data = s.loads(sec_openid)
    except BadData: # openid密文过期
        return None
    else:
        # 返回openid明文
        return data.get('openid')