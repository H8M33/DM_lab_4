import math
from bitarray import bitarray


class BloomFilter(object):

    def __init__(self, size, number_expected_elements=100000):
        self.size = size
        self.number_expected_elements = number_expected_elements

        self.bloom_filter = bitarray(self.size)
        self.bloom_filter.setall(0)

        self.number_hash_functions = round((self.size / self.number_expected_elements) * math.log(2))

    def _hash_djb2(self, s):
        _hash = 5381
        for x in s:
            _hash = ((_hash << 5) + _hash) + ord(x)
        return _hash % self.size

    def _hash(self, item, K):
        return self._hash_djb2(str(K) + item)

    def add_to_filter(self, item):
        for i in range(self.number_hash_functions):
            self.bloom_filter[self._hash(item, i)] = 1

    def check_is_not_in_filter(self, item):
        for i in range(self.number_hash_functions):
            if self.bloom_filter[self._hash(item, i)] == 0:
                return True
        return False


bloom_filter = BloomFilter(1000000, 100000)
text_str = open('text.txt').read().split()
for i in text_str:
    bloom_filter.add_to_filter(i)

# Проверими отсутствие в тексте слова 'tendrils'
print(bloom_filter.check_is_not_in_filter('tendrils'))
# Нам вернули значение False - это значит, что присутствует либо слово 'tendrils', либо другое слово, имеющее такое же знацение хэша
# Посмотрим, какое значение хэша у слова tendrils
# Для избегания ложноположиетльных срабатываний, мы берём несколько хэш функций, число которых зависит от объёма данных
print(bloom_filter.number_hash_functions, ' - количество хэш функций')
# Теперь посмотрим, какие значения должна принять каждая из этих функций, чтобы слово совпало по хэшу со словом 'tendrils'
for i in range(bloom_filter.number_hash_functions):
    print(bloom_filter._hash('tendrils', i))
# А теперь возьмём слово, которое гарантированно отсутствует в тексте и проверим, так ли это
print(bloom_filter.check_is_not_in_filter('bloom'))
# True - то, что мы и ожидали получить