from binary_num import Binary
from float_num import FloatPoint

def multiply_step_by_step(m, r, x = 32, y = 32):
    m = Binary(m, x)
    r = Binary(r, y)
    dim = x + y + 1

    A = Binary(m.get_value_list(), x + y + 1) << (y + 1) 
    S = Binary(m.get_self_negative_list(), x + y + 1) << (y + 1)
    P = Binary(r.get_value_list(), x + y + 1) << 1

    res = "Multiply using Booth`s algorithm\n"
    res += get_curent_state(0, "Initialization", dimention=dim, A=A, S=S, P=P)

    for i in range(1, y + 1):
        last_2_b = P.get_value_list()[-2:]
        action = "no action"
        if last_2_b[0] == 0 and last_2_b[1] == 1:
            action = "add A to P"
            P += A
        elif last_2_b[0] == 1 and last_2_b[1] == 0:
            action = "add S to P"
            P += S
        P.right_signed_shift()
        res += get_curent_state(i, "Loop", last_2_b=last_2_b, dimention=dim, action=action, A=A, S=S, P=P)
    P.right_signed_shift()
    P = Binary(P.get_value_list(), x + y)
    res += get_curent_state(y + 1, "Result", dimention=dim-1, result=P)

    return res

def multiply_binary(m, r):
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

def division_step_by_step(devidend, divisor, dim_ddend = 32, dim_dsor = 32):
    dsor = Binary(divisor, dim_dsor)
    dsor_neg = dsor.get_negative()
    rem = Binary(Binary.get_bin_list(devidend, dim_ddend), dim_ddend + dim_dsor)
    quot = Binary(0, devidend)

    res = "Division algorithm\n"
    res += get_curent_state(0, "Initialization", Divisor=dsor, Remainder=rem, Quotient=quot)

    curent_rem = Binary(0, dim_dsor)
    for i in range(dim_ddend):
        rem.left_shift()
        quot.left_shift()

        curent_rem.set_value(rem.get_value_list()[:dim_dsor])
        cur_sub_dsor = curent_rem + dsor_neg
        is_cur_ge_dsor = cur_sub_dsor.is_positive()

        if is_cur_ge_dsor:
            current_list = cur_sub_dsor.get_value_list() + rem.get_value_list()[dim_dsor:]
            rem.set_value(current_list)
            quot.add_one()

        res += get_curent_state(i, "Loop", Is_Rem_Greater = is_cur_ge_dsor, Remainder=rem, Quotient=quot)

    curent_rem.set_value(rem.get_value_list()[:dim_dsor])
    res += get_curent_state(dim_ddend, "Result", Remainder=curent_rem, Quotient=quot)

    return res

def division_binary(devidend, divisor):
    dim_dsor = divisor.get_dimention()
    dim_ddend = devidend.get_dimention()

    rem = Binary(devidend.get_value_list(), dim_ddend + dim_dsor)
    dsor_neg = divisor.get_negative()
    quot = Binary(0, devidend)

    res = "Division algorithm\n"
    res += get_curent_state(0, "Initialization", Divisor=divisor, Remainder=rem, Quotient=quot)

    curent_rem = Binary(0, dim_dsor)
    for i in range(dim_ddend):
        rem.left_shift()
        quot.left_shift()

        curent_rem.set_value(rem.get_value_list()[:dim_dsor])
        cur_sub_dsor = curent_rem + dsor_neg
        is_cur_ge_dsor = cur_sub_dsor.is_positive()

        if is_cur_ge_dsor:
            current_list = cur_sub_dsor.get_value_list() + rem.get_value_list()[dim_dsor:]
            rem.set_value(current_list)
            quot.add_one()

        res += get_curent_state(i, "Loop", Is_Rem_Greater = is_cur_ge_dsor, Remainder=rem, Quotient=quot)

    curent_rem.set_value(rem.get_value_list()[:dim_dsor])
    res += get_curent_state(dim_ddend, "Result", Remainder=curent_rem, Quotient=quot)

    return res


def get_curent_state(step, discription = "", dimention = 32,**kwargs):
    res = f"{step}. {discription} values:\n"
    for key in kwargs:
        val = kwargs[key]
        if isinstance(val, Binary):
            res += f"\t{key} = {val} or {val:b}\n"
        elif isinstance(val, FloatPoint):
            res += f"\t{key} = {val} or {val:bf}\n"
        else:
            res += f"\t{key} = {val}\n"

    return res

def get_float_mult(num1, num2):
    first = FloatPoint(num1)
    second = FloatPoint(num2)

    return first.step_by_step_mult(second, get_curent_state)

def main():
    with open("result.txt", "wb") as file:
        file.write(multiply_step_by_step( -23, 22).encode("utf-8"))

        file.write("\n".encode("utf-8"))
        file.write(" ".join("-" for i in range(30)).encode("utf-8"))
        file.write("\n".encode("utf-8"))

        file.write(division_step_by_step(125, 7).encode("utf-8"))

        file.write("\n".encode("utf-8"))
        file.write(" ".join("-" for i in range(30)).encode("utf-8"))
        file.write("\n".encode("utf-8"))

        file.write(get_float_mult(-213.23, 356.982).encode("utf-8"))

        file.write("\n".encode("utf-8"))
        file.write(" ".join("-" for i in range(30)).encode("utf-8"))
        file.write("\n".encode("utf-8"))
        
    

if __name__ == "__main__":
    main()