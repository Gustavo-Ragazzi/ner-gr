def validate_cpf(cpf: str) -> bool:
  cpf = cpf.replace(".", "").replace("-", "")
  if len(cpf) != 11 or not cpf.isdigit():
    return False
  if cpf == cpf[0] * 11:
    return False
  def calculate_digit(partial, weight):
    total = sum(int(d)*w for d, w in zip(partial, range(weight, 1, -1)))
    r = total % 11
    return '0' if r < 2 else str(11 - r)
  d1 = calculate_digit(cpf[:9], 10)
  d2 = calculate_digit(cpf[:9] + d1, 11)
  return cpf[-2:] == d1 + d2

def validate_cnpj(cnpj: str) -> bool:
  cnpj = cnpj.replace(".", "").replace("-", "").replace("/", "")
  if len(cnpj) != 14 or not cnpj.isdigit():
    return False
  if cnpj == cnpj[0] * 14:
    return False
  def calc(partial, weights):
    total = sum(int(d)*w for d, w in zip(partial, weights))
    r = total % 11
    return '0' if r < 2 else str(11 - r)
  w1 = [5,4,3,2,9,8,7,6,5,4,3,2]
  w2 = [6,5,4,3,2,9,8,7,6,5,4,3,2]
  d1 = calc(cnpj[:12], w1)
  d2 = calc(cnpj[:12] + d1, w2)
  return cnpj[-2:] == d1 + d2

def word2features(sent, i):
  word = sent[i][0]
  feats = {
    'bias': 1.0,
    'word.lower()': word.lower(),
    'word.isupper()': word.isupper(),
    'word.istitle()': word.istitle(),
    'word.isdigit()': word.isdigit(),
    'prefix-1': word[0],
    'suffix-1': word[-1],
    'prefix-2': word[:2],
    'suffix-2': word[-2:],
    'prefix-3': word[:3],
    'suffix-3': word[-3:],
    'is_cpf': validate_cpf(word),
    'is_cnpj': validate_cnpj(word)
  }
  if i > 0:
    w1 = sent[i-1][0]
    feats.update({
      '-1:word.lower()': w1.lower(),
      '-1:word.istitle()': w1.istitle(),
      '-1:word.isupper()': w1.isupper()
    })
  else:
    feats['BOS'] = True
  if i < len(sent)-1:
    w2 = sent[i+1][0]
    feats.update({
      '+1:word.lower()': w2.lower(),
      '+1:word.istitle()': w2.istitle(),
      '+1:word.isupper()': w2.isupper()
    })
  else:
    feats['EOS'] = True
  return feats

def sent2features(sent):
  return [word2features(sent, i) for i in range(len(sent))]
