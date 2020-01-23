

A_ = A{(s,w)>l,(n,e)>r}
U_,S_,V_ = svd(A_)
U = U_{l>(s,w),us>ne}
S = S_{us>sw,sv>ne}
V = V_{sv>sw,r>(n,e)}





with (s,w)>l,(n,e)>r:
    U,S,V = svd(A,(ne,sw,ne,sw))





U,S,V = A.svd((s,w),(n,e),(ne,sw,ne,sw))




A = U{ne} * {sw}S{ne} * {sw}V

A = U^ne * sw^S^ne * sw^V

A = (s,w)^U^ne * sw^S^ne * sw^V^(n,e)


"l"^re^"r" = ("l","d")^a^("r","u") * ("l","d")^b^("r","u")





Network MPS:
    Seq[Tensor] ts


proc canonize_mps(MPS mps1):
    






arg float H
arg float J
arg int SCALE
arg int CHI

A = ones_tensor((2,1,1,1,1),(o,l,r,u,d)) # a=0: spin=-1(down), a=1: spin=1(up)
B = ones_tensor((2,1,1,1,1),(o,l,r,u,d)) # b=0: spin=-1(down), b=1: spin=1(up)
L = dummy_diagonalTensor((1,1),(l,r))
R = dummy_diagonalTensor((1,1),(l,r))
U = dummy_diagonalTensor((1,1),(u,d))
D = dummy_diagonalTensor((1,1),(u,d))
PSI = twodim.Ptn2DCheckerBTPS(A,B,L,R,U,D, width_scale=scale, height_scale=scale)

# H = -hs-Jss
H1 = zeros_tensor((2,2),(o,i))
H1.data[0,0] = H
H1.data[1,1] = -H
H1 = Opn1DTMO(H1,[o,i],is_hermite=True)

H2 = zeros_tensor((2,2,2,2),["o0","o1","i0","i1"])
H2.data[0,0,0,0] = -J
H2.data[0,1,0,1] = J
H2.data[1,0,1,0] = J
H2.data[1,1,1,1] = -J
H2 = Opn1DTMO(H2,[["o0"],["o1"]],[["i0"],["i1"]],is_hermite=True)









