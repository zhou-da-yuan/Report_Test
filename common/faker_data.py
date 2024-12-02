import logging

from faker import Faker
# 获取 faker 的日志记录器并设置日志级别为 WARNING
logging.getLogger('faker').setLevel(logging.WARNING)


class CommonDataGenerator:
    def __init__(self, locale='zh_CN'):
        self.faker = Faker(locale)

    def ssn(self):
        """生成身份证号"""
        return self.faker.ssn()

    def bs(self):
        """随机公司服务名"""
        return self.faker.bs()

    def company(self):
        """随机公司名（长）"""
        return self.faker.company()

    def company_prefix(self):
        """随机公司名（短）"""
        return self.faker.company_prefix()

    def company_suffix(self):
        """公司性质"""
        return self.faker.company_suffix()

    def credit_card_expire(self):
        """随机信用卡到期日"""
        return self.faker.credit_card_expire()

    def credit_card_full(self):
        """生成完整信用卡信息"""
        return self.faker.credit_card_full()

    def credit_card_number(self):
        """信用卡号"""
        return self.faker.credit_card_number()

    def credit_card_provider(self):
        """信用卡类型"""
        return self.faker.credit_card_provider()

    def credit_card_security_code(self):
        """信用卡安全码"""
        return self.faker.credit_card_security_code()

    def job(self):
        """随机职位"""
        return self.faker.job()

    def first_name_female(self):
        """女性名"""
        return self.faker.first_name_female()

    def first_name_male(self):
        """男性名"""
        return self.faker.first_name_male()

    def last_name_female(self):
        """女姓"""
        return self.faker.last_name_female()

    def last_name_male(self):
        """男姓"""
        return self.faker.last_name_male()

    def name(self):
        """随机生成全名"""
        return self.faker.name()

    def name_female(self):
        """女性全名"""
        return self.faker.name_female()

    def name_male(self):
        """男性全名"""
        return self.faker.name_male()

    def phone_number(self):
        """随机生成手机号"""
        return self.faker.phone_number()

    def phonenumber_prefix(self):
        """随机生成手机号段"""
        # 注意：Faker 库没有直接提供手机号段的方法，这里需要模拟实现
        return self.faker.msisdn()[3:8]  # 假设前3位是国家代码，取后面的5位作为前缀


class RandomDataGenerator:
    def __init__(self, locale='zh_CN'):
        self.faker = Faker(locale)

    def numerify(self, x):
        text = '#'*x
        """生成x位随机数字"""
        return self.faker.numerify(text)

    def random_digit(self):
        """0~9随机数"""
        return self.faker.random_digit()

    def random_digit_not_null(self):
        """1~9的随机数"""
        return self.faker.random_digit_not_null()

    def random_int(self, min=0, max=9999):
        """随机数字，默认0~9999，可以通过设置min,max来设置"""
        return self.faker.random_int(min=min, max=max)

    def random_number(self, digits=None):
        """随机数字，参数digits设置生成的数字位数"""
        return self.faker.random_number(digits=digits)

    def pyfloat(self, left_digits=5, right_digits=2, positive=True):
        """生成浮点数，参数left_digits为整数部分位数，right_digits为小数部分位数，positive决定是否为正数"""
        return self.faker.pyfloat(left_digits=left_digits, right_digits=right_digits, positive=positive)

    def pyint(self, min_value=0, max_value=9999, step=1):
        """随机Int数字，参数min_value为最小值，max_value为最大值，step为步进"""
        return self.faker.pyint(min_value=min_value, max_value=max_value, step=step)

    def pydecimal(self, left_digits=5, right_digits=2, positive=True, max_value=None, min_value=None):
        """随机Decimal数字，参数left_digits为整数部分位数，right_digits为小数部分位数，positive决定是否为正数，max_value和min_value为值范围"""
        return self.faker.pydecimal(left_digits=left_digits, right_digits=right_digits, positive=positive,
                                    max_value=max_value, min_value=min_value)


class TimeDataGenerator:
    def __init__(self, locale='zh_CN'):
        self.faker = Faker(locale)

    def date(self):
        """随机日期"""
        return self.faker.date()

    def date_between(self, start_date='-30y', end_date='today'):
        """随机生成指定范围内日期，参数：start_date，end_date"""
        return self.faker.date_between(start_date=start_date, end_date=end_date)

    def date_between_dates(self, start_date='-30y', end_date='today'):
        """随机生成指定范围内日期，用法同上"""
        return self.faker.date_between_dates(date_start=start_date, date_end=end_date)

    def date_object(self, end_datetime=None):
        """随机生成从1970-1-1到指定日期的随机日期。"""
        return self.faker.date_object(end_datetime=end_datetime)

    def date_time(self):
        """随机生成指定时间（1970年1月1日至今）"""
        return self.faker.date_time()

    def date_time_ad(self):
        """生成公元1年到现在的随机时间"""
        return self.faker.date_time_ad()

    def date_time_between(self, start_date='-30y', end_date='now'):
        """用法同dates"""
        return self.faker.date_time_between(start_date=start_date, end_date=end_date)

    def future_date(self, end_date='+30d'):
        """未来日期"""
        return self.faker.future_date(end_date=end_date)

    def future_datetime(self, end_date='+30d'):
        """未来时间"""
        return self.faker.future_datetime(end_date=end_date)

    def month(self):
        """随机月份"""
        return self.faker.month()

    def month_name(self):
        """随机月份（英文）"""
        return self.faker.month_name()

    def past_date(self, start_date='-30d'):
        """随机生成已经过去的日期"""
        return self.faker.past_date(start_date=start_date)

    def past_datetime(self, start_date='-30d'):
        """随机生成已经过去的时间"""
        return self.faker.past_datetime(start_date=start_date)

    def time(self):
        """随机24小时时间"""
        return self.faker.time()

    def timedelta(self, start_datetime=None, end_datetime=None):
        """随机获取时间差"""
        return self.faker.time_delta(start_datetime=start_datetime, end_datetime=end_datetime)

    def time_object(self):
        """随机24小时时间，time对象"""
        return self.faker.time_object()

    def time_series(self, start_date='-30d', end_date='today', precision='day'):
        """随机TimeSeries对象"""
        return self.faker.time_series(start_date=start_date, end_date=end_date, precision=precision)

    def timezone(self):
        """随机时区"""
        return self.faker.timezone()

    def unix_time(self, start_datetime=None, end_datetime=None):
        """随机Unix时间"""
        return self.faker.unix_time(start_datetime=start_datetime, end_datetime=end_datetime)

    def year(self):
        """随机年份"""
        return self.faker.year()


if __name__ == '__main__':
    print(RandomDataGenerator().numerify(11))