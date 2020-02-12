from binary_num import Binary

class FloatPoint:

    def __init__(self, number):
        if number == 0:
            self.__val = 0
            self.__sign = 0
            self.__power = [0 for i in range(FloatPoint.get_power_len())]
            self.__mantisa = [0 for i in range(FloatPoint.get_mantisa_len())]
        else:
            self.__val = None
            self.__sign = None
            self.__power = None
            self.__mantisa = None

            self.set_value(number)

    def is_zero(self):
        return all(i == 0 for i in self.__power)

    def set_value(self, value):
        self.__val = value
        self.__sign = 0 if value > 0 else 1
        self.__power = FloatPoint.get_num_power(value)
        self.__mantisa = FloatPoint.get_num_mantisa(value)

    def get_calculeted_value(self):
        if self.is_zero():
            return 0
        return FloatPoint.calc_value_from_binary(self.__sign, self.__power, self.__mantisa)

    def __mul__(self, other):
        if self.is_zero() or other.is_zero():
            return FloatPoint(0)
        res = FloatPoint(1)
        res.__sign = 0 if self.__sign == other.__sign else 1
        res.__mantisa, is_power_shifted = FloatPoint.get_mantisa_lists_mult(self.__mantisa, other.__mantisa)

        res.__power = FloatPoint.add_power_lists(self.__power, other.__power)
        if is_power_shifted:
            Binary.add_one_to_list(res.__power) 

        return res

    def step_by_step_mult(self, other, res_func):
        if self.is_zero() or other.is_zero():
            return  res_func(1, "One of them zero", First=self, Second=other, Res=FloatPoint(0))
        res = FloatPoint(1)
        res.__sign = 0 if self.__sign == other.__sign else 1
        total = res_func(1, "Sign", First=self.__sign, Second=other.__sign, Res=res.__sign)

        res.__mantisa, is_power_shifted = FloatPoint.get_mantisa_lists_mult(self.__mantisa, other.__mantisa)
        total += res_func(2, "Mantisa", First="".join(str(i) for i in self.__mantisa), 
            Second="".join(str(i) for i in other.__mantisa), Res="".join(str(i) for i in res.__mantisa))
        
        res.__power = FloatPoint.add_power_lists(self.__power, other.__power)
        if is_power_shifted:
            Binary.add_one_to_list(res.__power) 
        total += res_func(3, "Power", Is_power_need_add=is_power_shifted,First="".join(str(i) for i in self.__power), 
            Second="".join(str(i) for i in other.__power), Res="".join(str(i) for i in res.__power))    

        res.__val = FloatPoint.calc_value_from_binary(res.__sign, res.__power, res.__mantisa)
        total += res_func(4, "Total", First=self, Second=other, Res=res)

        return total

    def __str__(self):
        return str(self.__val)

    def __format__(self, spec):
        if spec == "b":
            res = "1" if self.__sign else "0"
            res += "  "

            res += "".join("1" if i else "0" for i in self.__power)
            res += "  "

            leng = len(self.__mantisa)
            pos = 0
            is_start_print = False

            while pos < leng:
                val = self.__mantisa[pos]

                if not is_start_print:
                    if val == 1:
                        is_start_print = True
                
                if is_start_print:
                    if (leng - pos) % 8 == 0:
                        res += " "

                    if (leng - pos) % 4 == 0:
                        res += " "
                    res += "1" if val else "0"
                
                pos += 1

            return res
        elif spec == "bf":
            res = "1" if self.__sign else "0"
            res += "  "

            res += "".join("1" if i else "0" for i in self.__power)
            res += "  "

            leng = len(self.__mantisa)
            pos = 0

            while pos < leng:
                val = self.__mantisa[pos]
                
                if (leng - pos) % 8 == 0:
                    res += " "

                if (leng - pos) % 4 == 0:
                    res += " "
                res += "1" if val else "0"
                
                pos += 1

            return res
        else:
            return self.__str__()

    @staticmethod
    def calc_value_from_binary(sign, power, mantisa):
        power = FloatPoint.get_true_power(power)
        abs_val = 0
        if power > 0:
            if power < FloatPoint.get_mantisa_len():
                abs_val = Binary.get_positive_list_value([1] + mantisa[:power])
                abs_val += FloatPoint.get_float_value(mantisa[power:])
            else:
                abs_val = Binary.get_positive_list_value([1] + mantisa + [0 for i in range(power - FloatPoint.get_mantisa_len())])
        elif power == 0:
            abs_val = 1 + FloatPoint.get_float_value(mantisa)
        else:
            abs_val = FloatPoint.get_float_value([0 for i in range(-power - 1)] + [1] + mantisa)
            
        return -abs_val if sign else abs_val

    @staticmethod
    def get_true_power(power_list):
        ng_middle = Binary.get_negative_list(FloatPoint.get_middle_power_list())
        true_pow_fir = Binary.get_lists_add(power_list, ng_middle)
        return Binary.get_num_from_bit_list(true_pow_fir)

    @staticmethod
    def get_mantisa_lists_mult(first, second):
        first = [0, 1] + first
        second = [0, 1] + second

        f_bin = Binary(first, len(first))
        s_bin = Binary(second, len(second))
        res_list = (f_bin * s_bin).get_value_list()
        ind_1 = res_list.index(1)

        need_add_power = res_list[2] == 1
        res_list = res_list[ind_1 + 1:]

        return res_list[:FloatPoint.get_mantisa_len()], need_add_power

    @staticmethod
    def add_power_lists(first, second):
        ng_middle = Binary.get_negative_list(FloatPoint.get_middle_power_list())
        true_pow_fir = Binary.get_lists_add(first, ng_middle)
        return Binary.get_lists_add(true_pow_fir, second)

    @staticmethod
    def get_middle_power_list():
        return [0, 1, 1, 1, 1, 1, 1, 1]

    @staticmethod
    def get_middle_power_int():
        return 127

    @staticmethod
    def get_mantisa_len():
        return 23

    @staticmethod
    def get_power_len():
        return 8

    @staticmethod
    def get_num_mantisa(num):
        num = abs(num)
        if num >= 1:
            return FloatPoint.get_num_ge1_mantisa(num)
        else:
            return FloatPoint.get_num_lt1_mantisa(num)

    @staticmethod
    def get_num_lt1_mantisa(num, leng=None, is_remove_zero_and_first_1=True):
        if not leng:
            leng = FloatPoint.get_mantisa_len()
        if is_remove_zero_and_first_1:
            while num < 1:
                num *= 2
            num %= 1
        res = []
        for i in range(leng):
            num *= 2
            res.append(1 if num >= 1 else 0)
            num %= 1
        return res

    @staticmethod
    def get_num_power(num):
        num = abs(num)
        tr_pow = FloatPoint.get_num_ge1_power(num) if num > 1 else FloatPoint.get_num_lt1_power(num)
        tr_pow_l = Binary.get_bin_list(tr_pow, FloatPoint.get_power_len())
        power =  Binary.get_lists_add(tr_pow_l, FloatPoint.get_middle_power_list())
        return power
    
    @staticmethod
    def get_num_ge1_mantisa(num):
        res = []
        num_ge1 = num // 1
        while num_ge1 > 0:
            res.insert(0, 1 if num_ge1 % 2 == 1 else 0)
            num_ge1 //= 2
        mant_len = FloatPoint.get_mantisa_len()
        res = res[res.index(1) + 1:]
        
        if len(res) < mant_len:
            temp = FloatPoint.get_num_lt1_mantisa(num % 1, mant_len - len(res), False)
            res.extend(temp)
        else:
            res = res[:23]
        return res

    @staticmethod
    def get_num_ge1_power(num):
        i = -1
        while num > 0:
            num //= 2
            i += 1
        return i

    @staticmethod
    def get_num_lt1_power(num):
        i = 0
        while num < 1:
            num *= 2
            i -= 1
        return i

    @staticmethod
    def get_float_value(val_list):
        res = 0
        for i in range(len(val_list) - 1, -1, -1):
            res += val_list[i]
            res /= 2
        return res


if __name__ == "__main__":
    point = FloatPoint(228)
    po = FloatPoint(1.1111111)
    r = point * po
    print(f"{r:bf}")
    print(r.get_calculeted_value())