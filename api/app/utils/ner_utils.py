from typing import List, Tuple, Dict, Union


def validate_cpf(cpf: str) -> bool:
  """
  Validates a Brazilian CPF number.

  Args:
    cpf (str): CPF string (may contain punctuation)

  Returns:
    bool: True if valid, False otherwise
  """
  cpf = cpf.replace(".", "").replace("-", "")
  if len(cpf) != 11 or not cpf.isdigit():
    return False
  if cpf == cpf[0] * 11:
    return False

  def calculate_digit(partial: str, weight: int) -> str:
    total = sum(int(d) * w for d, w in zip(partial, range(weight, 1, -1)))
    r = total % 11
    return '0' if r < 2 else str(11 - r)

  d1 = calculate_digit(cpf[:9], 10)
  d2 = calculate_digit(cpf[:9] + d1, 11)
  return cpf[-2:] == d1 + d2


def validate_cnpj(cnpj: str) -> bool:
  """
  Validates a Brazilian CNPJ number.

  Args:
    cnpj (str): CNPJ string (may contain punctuation)

  Returns:
    bool: True if valid, False otherwise
  """
  cnpj = cnpj.replace(".", "").replace("-", "").replace("/", "")
  if len(cnpj) != 14 or not cnpj.isdigit():
    return False
  if cnpj == cnpj[0] * 14:
    return False

  def calc(partial: str, weights: List[int]) -> str:
    total = sum(int(d) * w for d, w in zip(partial, weights))
    r = total % 11
    return '0' if r < 2 else str(11 - r)

  w1 = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
  w2 = [6, 5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]

  d1 = calc(cnpj[:12], w1)
  d2 = calc(cnpj[:12] + d1, w2)
  return cnpj[-2:] == d1 + d2

def word2features(sent: List[Tuple[str, str]], i: int) -> Dict[str, Union[str, bool, float]]:
  """
  Extracts CRF-compatible features for the word at position i in a sentence.

  Args:
    sent (List[Tuple[str, str]]): Sentence as list of (token, label) tuples
    i (int): Position of the target token

  Returns:
    Dict[str, Union[str, bool, float]]: Feature dictionary for the token
  """
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
    prev_word = sent[i - 1][0]
    feats.update({
      '-1:word.lower()': prev_word.lower(),
      '-1:word.istitle()': prev_word.istitle(),
      '-1:word.isupper()': prev_word.isupper()
    })
  else:
    feats['BOS'] = True  # Beginning of sentence

  if i < len(sent) - 1:
    next_word = sent[i + 1][0]
    feats.update({
      '+1:word.lower()': next_word.lower(),
      '+1:word.istitle()': next_word.istitle(),
      '+1:word.isupper()': next_word.isupper()
    })
  else:
    feats['EOS'] = True  # End of sentence

  return feats


def sent2features(sent: List[Tuple[str, str]]) -> List[Dict[str, Union[str, bool, float]]]:
  """
  Extract features for every word in a sentence.

  Args:
    sent (List[Tuple[str, str]]): Sentence as list of (token, label) tuples

  Returns:
    List[Dict[str, Union[str, bool, float]]]: List of feature dictionaries
  """
  return [word2features(sent, i) for i in range(len(sent))]
