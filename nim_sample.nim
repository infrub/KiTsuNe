var a = 1
var b: int
var c = 1+2*3+4
b = a * c
echo b

proc f(x:int):int =
    var y = x*2
    return y+1

echo(f(1))