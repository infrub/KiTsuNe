type MPS = object
  tensors: seq[Tensor["l","r","o"]]
  weight: PowComplex

proc len(phi:MPS):int = phi.tensors.len

type MPO = object
  tensors: seq[Tensor["l","r","i","o"]]
  weight: PowComplex

proc len(gate:MPO):int = gate.tensors.len




proc apply(phi: MPS, gate: MPO, offset:int):MPS =
  result = newSeq[Tensor["l","r","o"]]()
  for i in phi.len:
    var re: Tensor["l","r","o"]
    if i<offset:
      re = phi[i]
    elif i<offset+mpo.len:
      re = ( phi[i]^"o" * "i"^gate[i] ){("l","l")>"l", ("r","r")>"r"}
    else:
      re = phi[i]
    result.add re



