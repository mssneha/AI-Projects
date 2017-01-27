from collections import defaultdict, Sequence
from copy import deepcopy
import itertools

class nameSpace(defaultdict):
	def __missing__(self, k):
		res = self.default_factory(k)
		self[k] = res
		return res


class ParRule:
	def __init__(self, operator, left):
		self.operator = operator
		self.left = left

	def __or__(self, right):
		return Rule(self.operator, self.left, right)

	def __repr__(self): 
		return "ParRule('{}',{})".format(self.operator, self.left)


class Rule:
	def __init__(self, operator, *arguments):
		self.operator = operator
		self.arguments = arguments

	def __and__(self, right):
		return Rule("&", self, right)

	def __or__(self, right):
		if isinstance(right, Rule):
			return Rule("|", self, right)
		else:
			return ParRule(right, self)

	def __invert__(self):
		return Rule("~", self)

	def __rand__(self, left): 
		return Rule("&", left, self)

	def __ror__(self, left): 
		return Rule("|", left, self)

	def __eq__(self, rem):
		if isinstance(rem, Rule) and self.operator == rem.operator and self.arguments == rem.arguments:
			return True
		else:
			return False

	def __hash__(self):
		return hash(self.operator) ^ hash(self.arguments)

	def __ne__(self, rem):
		return not self.__eq__(rem)

	def __call__(self, *arguments):
		return Rule(self.operator, arguments)

	def __repr__(self):
		operands = [str(operand) for operand in self.arguments]
		if isIdentifier(self.operator):
			return '{}({})'.format(self.operator, ', '.join(operands)) if operands else self.operator
		elif len(operands) == 1:
			return self.operator + operands[0]
		else:
			return "(" + (" " + str(self.operator) + " ").join(operands) + ")"


class knowBase:
	def __init__(self, kb_rules = None):
		self.kb_rules = []
		self.ruleNo = dict()
		if kb_rules:
			for p_r in kb_rules:
				self.tellKB(p_r)

	def addRuleNo(self, pred, rNo): 
		if pred not in self.ruleNo:
			self.ruleNo[pred] = set()
			self.ruleNo[pred].add(rNo)
		else:
			self.ruleNo[pred].add(rNo)		

	def tellKB(self, kb_rule):
		self.kb_rules.append(kb_rule)
		preds = set(getPredicates(kb_rule))
		for pred in preds:
			self.addRuleNo(pred, len(self.kb_rules) - 1)

	def askKB(self, kb_rule):
		return resolution(self, kb_rule)

	def rulesWPredicate(self, pred):
		rulesWpred = []
		if pred in self.ruleNo:
			for r in self.ruleNo[pred]:
				rulesWpred.append(self.kb_rules[r])
		return set(rulesWpred)

	def rulesWhResolve(self, kb_rule):
		rulesWhRes = set()
		preds =  getPredicates(kb_rule)
		for pred in preds:
			if pred[0] != "~":
				pred = "~" + pred
			else:
				pred = pred[1:]
			rulesWhRes = rulesWhRes.union(self.rulesWPredicate(pred))
		return rulesWhRes

def symb(symbol):
	return Rule(symbol)

def buildRule(ele_rule):
	if isinstance(ele_rule, str):
		ele_rule = ele_rule.replace("=>", "|" + repr("=>") +"|") 
		return eval(ele_rule , nameSpace(symb))

def isIdentifier(sym):
	if isinstance(sym, str):
		if sym[0].isalpha():
			return True
	return False

def isVar(sym):
	if isinstance(sym, Rule):
		if not sym.arguments:
			if sym.operator[0].islower():
				return True
	return False

def isPredOrConst(p_rule):
	if isinstance(p_rule, str) and p_rule.isalpha() and p_rule[0].isupper():
		return True
	return False

def isVarSymb(sym): 
	if isinstance(sym, str):
		if sym[0].isalpha():
			if sym[0].islower():
				return True
	return False

def getPredicates(sentence, negated = False):
	predicates = []
	if isinstance(sentence, Rule):
		if isinstance(sentence.operator, str) and sentence.operator.isalpha() and sentence.operator[0].isupper() and len(sentence.arguments) >= 1:
			predicates.append(sentence.operator if not negated else "~" + sentence.operator)
		else:
			for operand in sentence.arguments:
				predicates += getPredicates(operand, True if sentence.operator == "~" else False)
	return predicates

def splitRules(operator, s): 
	args = []
	for arg in s:
		if arg.operator == operator: 
			for a in splitRules(operator, arg.arguments):
				args.append(a)
		else:
			args.append(arg)
	return args

def groupRules(operator, arguments):
	args = splitRules(operator, arguments)
	if len(arguments) == 1:
		return arguments[0]
	if len(arguments) == 0:
		return False
	else:
		return Rule(operator, *arguments)

def removeImplication(p_rule):
	args = []
	if not p_rule.arguments or isPredOrConst(p_rule.operator):
		return p_rule
	for arg in p_rule.arguments: 
		args.append(removeImplication(arg))
 
	if p_rule.operator == "=>": 
		p = ~args[0]
		q = args[1]
		return p | q

	else:
		return Rule(p_rule.operator, *args)

def negate(p_rule):
	if p_rule.operator == "~":
		neg_arg = p_rule.arguments[0]
		if neg_arg.operator == "|": 
			args = []
			for arg in neg_arg.arguments:
				args.append(negate(~arg))
			return groupRules("&", args)
		elif neg_arg.operator == "&":
			args = []
			for arg in neg_arg.arguments:
				args.append(negate(~arg))
			return groupRules("|", args)
		elif neg_arg.operator == "~":
			return negate(neg_arg.arguments[0])
		return p_rule
	elif not p_rule.arguments or isPredOrConst(p_rule.operator):
		return p_rule
	else:
		args = []
		for arg in p_rule.arguments: 
			args.append(negate(arg))
		return Rule(p_rule.operator, *args)

def distribute(p_rule):
	if p_rule.operator == "|":
		p_rule = groupRules("|", p_rule.arguments)
		if p_rule.operator != "|":
			return distribute(p_rule)
		else:
			if len(p_rule.arguments) == 1:
				return distribute(p_rule.arguments[0])
			else: 
				conjunction = None
				for arg in p_rule.arguments:
					if arg.operator == "&":
						conjunction = arg 
						break
				if conjunction == None:
					return p_rule
				else:
					nonConjunctions = []
					for arg in p_rule.arguments:
						if arg is not conjunction:
							nonConjunctions.append(arg)

					nonConjunctions = groupRules("|", nonConjunctions)

					res =[]

					for conjunct in conjunction.arguments:
						res.append(distribute(conjunct | nonConjunctions))

					return groupRules("&", res)

	elif p_rule.operator == "&":
		args = []
		for arg in p_rule.arguments:
			args.append(distribute(arg))
		return groupRules("&", args)

	else:
		return p_rule

def standardize(p_rule, varDict = None): 
	if varDict == None:
		varDict = {}

	if not isinstance(p_rule, Rule):
		if isinstance(p_rule, tuple):
			return tuple(standardize(arg, varDict) for arg in p_rule)
		else:
			return p_rule
	elif isVarSymb(p_rule.operator):
		if p_rule in varDict:
			return varDict[p_rule]
		else:
			var = Rule('{}{}'.format(p_rule.operator, next(standardize.count)))
			varDict[p_rule] = var
			return var
	else:
		return Rule(p_rule.operator, *[standardize(s, varDict) for s in p_rule.arguments])

standardize.count = itertools.count()

def remEle(i, seq): 
	res = []
	for s in seq:
		if s != i:
			res.append(s)
	return res


def unifyVar(var, val, theta): 
	if var in theta:
		return unify(theta[var], val, theta)
	else:
		subst = deepcopy(theta)
		subst[var] = val
		return subst
		

def unify(x, y, theta):
	if theta is None:
		return None
	elif x == y:
		return theta
	elif isVar(x):
		return unifyVar(x, y, theta)
	elif isVar(y):
		return unifyVar(y, x, theta)
	
	elif isinstance(x, Sequence) and isinstance(y, Sequence): 
		if len(y) == len(x):
			if not isinstance(y, str):
				if not isinstance(x,str):
					return unify(x[1:], y[1:], unify(x[0], y[0], theta))
		else:
			return None
	elif isinstance(x, Rule):
		if isinstance(y, Rule):
			t = unify(x.operator, y.operator, theta)
			return unify(x.arguments, y.arguments, t)

	else:
		return None

def subst(s, x):
    if isinstance(x, list):
        return [subst(s, xi) for xi in x]
    elif isinstance(x, tuple):
        return tuple([subst(s, xi) for xi in x])
    elif not isinstance(x, Rule):
        return x
    elif isVarSymb(x.operator):
        return s.get(x, x)
    else:
        return Rule(x.operator, *[subst(s, arg) for arg in x.arguments])

def remDups(p_rule):
	n = len(p_rule)
	l = list(p_rule)
	y = []
	rem = []
	for p in range(0, n):
		y.append(set(splitRules("|", [l[p]])))

	for p in range(0, n):
		z = set(splitRules("|", [l[p]]))
		for q in range(p + 1, n):
			if z == y[q]:
				rem.append(p)

	for i in sorted(set(rem), reverse = True):
		del l[i]
	return set(p_rule)


def resMatchingRules(rule1, rule2):
	new_rules= []
	rule1Dis = splitRules("|", [rule1])
	rule2Dis = splitRules("|", [rule2])
	for d1 in rule1Dis:
		for d2 in rule2Dis:
			theta = dict()
			if d2.operator == "~":
				theta = unify(d1, d2.arguments[0], theta)
			elif d1.operator == "~":
				theta = unify(d1.arguments[0], d2, theta)
			if theta is not None:
				d1 = subst(theta, d1)
				d2 = subst(theta, d2)
				if ~d1 == d2 or d1 == ~d2:
					rule2Dis = subst(theta, rule2Dis)
					rule1Dis = subst(theta, rule1Dis)
					afterRemEle1 = remEle(d1, rule1Dis)
					afterRemEle2 = remEle(d2, rule2Dis)
					s = set(afterRemEle1 + afterRemEle2)
					newList = list(s)
					g = groupRules("|", newList)
					new_rules.append(g)
	return new_rules

def negateQuery(query):
	op_list = getPredicates(query)
	if op_list[0][0] == '~':
		return query.arguments[0]
	return ~query

def resolution(kb, query): 
	org_rules = kb.kb_rules
	kb_rules_w_query = org_rules + [negateQuery(query)]
	new_KB = knowBase(kb_rules_w_query)
	new_rules = set()
	while True:
		matchingRules = []
		l = len(new_KB.kb_rules)
		for p in range(l):
			rulesWhRes = new_KB.rulesWhResolve(new_KB.kb_rules[p])
			for q in range(p + 1, l):
				if new_KB.kb_rules[q] in rulesWhRes:
					matchingRules.append((new_KB.kb_rules[p], new_KB.kb_rules[q]))
		for (rule1, rule2) in matchingRules:
			resolvedRules = resMatchingRules(rule1, rule2)
			if False in resolvedRules:
				return True
			new_rules = new_rules.union(set(resolvedRules))
		new_rules = remDups(new_rules)

		if new_rules.issubset(set(new_KB.kb_rules)):
			return False

		if len(new_rules) > 5000:
			return False

		for new_rule in new_rules:
			if new_rule not in new_KB.kb_rules:
				new_KB.tellKB(new_rule)


def convertToCNF():
	sentAfterCNF = []
	for i in range(no_of_rules):
		s = removeImplication(ruleList[i])
		s = negate(s)
		s = distribute(s)
		sentAfterCNF.append(s)
	return sentAfterCNF

f_in = open("input.txt", "r")

queryList = []
ruleList = []

no_of_queries = int(f_in.readline().rstrip('\n').strip())
for i in range(no_of_queries):
	query = f_in.readline().rstrip('\n').strip()
	queryList.append(buildRule(query))

no_of_rules = int(f_in.readline().rstrip('\n').strip())
for i in range(no_of_rules):
	sentence = f_in.readline().rstrip('\n').strip()
	ruleList.append(buildRule(sentence))

sentAfterCNF = convertToCNF()

rulesAfterStandardize = []

for s in sentAfterCNF:
	conjList = splitRules("&", [s])
	for conj in conjList:
		s = standardize(conj)
		rulesAfterStandardize.append(s) 


fOut = open("output.txt", "w")

kb = knowBase()
for r in rulesAfterStandardize:
	kb.tellKB(r)

for query in queryList:
	result = kb.askKB(query)
	res = str(result)
	fOut.write(res.upper())
	fOut.write("\n")
	print(res)

fOut.close()




