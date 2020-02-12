class Binary:
    def __init__(self, value, dimention, signed = True):
        self.__signed = signed
        self.__val = None
        self.__dim = dimention
        self.__value_list = None

        self.set_value(value)
        
    def __add__(self, other):
        if self.__signed != other.__signed:
            raise Exception("addition of signed and not signed nums not supported")
        return Binary(self.__val + other.__val, self.__dim if self.__dim >= other.__dim else other.__dim)
    
    def add_one(self):
        lis = self.__value_list
        for i in range(self.__dim - 1, -1, -1):
            if lis[i] == 0:
                lis[i] = 1
                break
            else:
                lis[i] = 0
        self.__val = Binary.get_num_from_bit_list(lis) 

    def set_value(self, value):
        if isinstance(value, list):
            self.set_value_list(value)
        elif isinstance(value, int):
            self.set_value_int(value)

    def set_value_list(self, value):
        len_val = len(value)
        if len_val > self.__dim:
            value = value[len_val - self.__dim:]
        elif len_val < self.__dim:
            temp = [0 for i in range(self.__dim - len_val)]
            value = temp + value
        if self.__signed:
            self.__val = Binary.get_num_from_bit_list(value)
        else:
            self.__val = Binary.get_positive_list_value(value)
        self.__value_list = value

    def set_value_int(self, value):
        if (not self.__signed) and value < 0:
            raise Exception("Unsigned binary can`t be less then zero")
        value = value % (1 << self.__dim)
        self.__value_list = Binary.get_bin_list(value, self.__dim)
        if self.__signed:
            self.__val = Binary.get_num_from_bit_list(self.__value_list)
        else:
            self.__val = value

    def get_value(self):
        return self.__val

    def get_value_list(self):
        return list(self.__value_list)

    def get_dimention(self):
        return self.__dim

    def left_shift(self):
        val_list = self.__value_list

        for i in range(len(val_list) - 1):
            val_list[i] = val_list[i + 1]

        val_list[len(val_list) - 1] = 0
        self.__val = Binary.get_num_from_bit_list(val_list)

    def right_signed_shift(self):
        val_list = self.__value_list

        for i in range(len(val_list) - 1, 0, -1):
            val_list[i] = val_list[i - 1]
        self.__val = Binary.get_num_from_bit_list(val_list)

    def get_negative(self):
        res = Binary(-1 * self.__val, self.__dim)
        return res

    def get_self_negative_list(self):
        return Binary.get_negative_list(self.__value_list)

    def __str__(self):
        return str(self.__val)

    def __format__(self, spec):
        if spec == "b":
            leng = len(self.__value_list)
            pos = 0
            is_start_print = False
            res = ""

            while pos < leng:
                val = self.__value_list[pos]

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

            if len(res) < 1:
                res = "0"

            return res
        else:
            return self.__str__()

    def __lshift__(self, num):
        res = Binary(self.__val, self.__dim)
        if num > 0:
            for i in range(num):
                res.left_shift()
        elif num < 0:
            for i in range(abs(num)):
                res.right_signed_shift()
        
        return res

    def __rshift__(self, num):
        res = Binary(self.__val, self.__dim)
        if num > 0:
            for i in range(num):
                res.right_signed_shift()
        elif num < 0:
            for i in range(abs(num)):
                res.left_shift()
        
        return res

    def is_negative(self):
        return True if self.__value_list[0] == 1 else False

    def is_positive(self):
        return True if self.__value_list[0] == 0 else False

    def __mul__(self, other):
        m = self
        r = other
        x = m.get_dimention()
        y = r.get_dimention()

        dim = x + y + 1

        A = Binary(m.get_value_list(), x + y + 1) << (y + 1) 
        S = Binary(m.get_self_negative_list(), x + y + 1) << (y + 1)
        P = Binary(r.get_value_list(), x + y + 1) << 1

        for i in range(1, y + 1):
            last_2_b = P.get_value_list()[-2:]

            if last_2_b[0] == 0 and last_2_b[1] == 1:
                P += A
            elif last_2_b[0] == 1 and last_2_b[1] == 0:
                P += S
            P.right_signed_shift()
        P.right_signed_shift()
        P = Binary(P.get_value_list(), x + y)

        return P

    @staticmethod
    def get_num_from_bit_list(bit_list):
        res = 1
        if bit_list[0] == 1:
            res = -1
            bit_list = Binary.get_negative_list(bit_list)
        
        res *= Binary.get_positive_list_value(bit_list)

        return res
        
    @staticmethod
    def get_positive_list_value(bin_list):
        res = 0
        for i in range(len(bin_list)):
            res <<= 1
            res += bin_list[i]
        return res

    @staticmethod
    def get_negative_list(bit_list):
        res = []
        for i in range(len(bit_list)):
            res.append(0 if bit_list[i] == 1 else 1)
        
        for i in range(len(res) - 1, -1, -1):
            if res[i] == 0:
                res[i] = 1
                break
            else:
                res[i] = 0
        
        return res

    @staticmethod
    def get_bin_list(num, dimention):
        if num < 0:
            return Binary.get_bin_negative_list(num, dimention)
        else:
            return Binary.get_bin_positive_list(num, dimention)

    @staticmethod
    def get_bin_positive_list(num, dimention):
        res = []
        for i in range(dimention):
            res.insert(0, num % 2)
            num //= 2
        return res
    
    @staticmethod
    def get_bin_negative_list(num, dimention):
        num = abs(num)
        res = []
        for i in range(dimention):
            res.insert(0, (num + 1) % 2)
            num //= 2

        for i in range(dimention - 1, -1, -1):
            if res[i] == 0:
                res[i] = 1
                break
            else:
                res[i] = 0

        return res

    @staticmethod
    def get_lists_add(first, second):#not debugged
        len_fir = len(first)
        len_sec = len(second)
        res_len = len_fir

        if len_fir > len_sec:
            second = [0 for i in range(len_fir - len_sec)] + second
        elif len_sec > len_fir:
            first = [0 for i in range(len_sec - len_fir)] + first
            res_len = len_sec

        res = []
        c = 0
        for i in range(res_len - 1, -1, -1):
            curr_sum = c + first[i] + second[i]
            res.insert(0, curr_sum % 2)
            c = curr_sum // 2
        
        return res

    @staticmethod
    def add_one_to_list(bin_list):
        for i in range(len(bin_list) - 1, -1, -1):
            if bin_list[i] == 0:
                bin_list[i] = 1
                break
            else:
                bin_list[i] = 0

if __name__ == "__main__":
    first = [1, 1, 1, 1]
    print(Binary(first, 4))
    second = [1, 0, 1, 0]
    print(Binary(second, 4))
    add = Binary.get_lists_add(first, second)
    print(Binary(add, 4))