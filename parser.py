"""
Grammar used for the parser 
Stmt_list       ->      Stmt Stmt_list | ε.
Stmt            ->      id = Expr | print Expr.
Expr            ->      Term Term_tail.
Term_tail       ->      First_priority Term Term_tail | ε.
Term            ->      Factor Factor_tail.
Factor_tail     ->      Second_priority Factor Factor_tail | ε.
Factor          ->      (Expr) | id | boolean.
First_priority  ->      not| ε.
Second_priority ->      and | or .

FIRST sets 
----------
Stmt_list		id,print,ε
Stmt			id print	
Expr			(,id,boolean	
Term_tail		not,ε
Term			(,id,boolean	
Factor_tail		ε,and or	
Factor			(,id,boolean	
First_priority	ε,not	
Second_priority	and,or

FOLLOW sets
-----------
Stmt_list		∅	
Stmt			∅	
Expr			)	
Term_tail		)	
Term			not	
Factor_tail		not	
Factor			and ,or
First_priority		)
Second_priority		)	
"""



from plex import *



class ParseError(Exception):
	""" A user defined exception class, to describe parse errors. """
	pass



class MyParser:
	""" A class encapsulating all parsing functionality
	for a particular grammar. """
	
	def create_scanner(self,fp):
		""" Creates a plex scanner for a particular grammar 
		to operate on file object fp. """

		# define some pattern constructs
		letter = Range("AZaz")
		digit  = Range("09")

		name  = letter + Rep(letter | digit)
		space = Rep1(Any(" \t\n"))
		# Logical strings
		notToken = Str("not")
		andToken = Str("and")
		orToken  = Str("or")
		equalSign = Str("=")
		#Boolean strings
		boolean_first= NoCase(Str("true", "t", "1"))
		boolean_second = NoCase(Str("false", "f", "0"))
		
		lexicon = Lexicon([
				(boolean_first, "Got a TRUE"),
				(boolean_second, "Got a FALSE"),			
				(equalSign, "Got an EQUAL_SIGN"),
				(notToken, "Got a NOT"),
				(andToken, "Got an AND"),
				(orToken, "Got an OR"),
				(name, "Identifier"),
				(space, IGNORE)
		])


		# create and store the scanner object
		self.scanner = Scanner(lexicon,fp)
		
		# get initial lookahead
		self.la,self.val = self.next_token()


	def next_token(self):
		""" Returns tuple (next_token,matched-text). """
		
		return self.scanner.read()		

	
	def position(self):
		""" Utility function that returns position in text in case of errors.
		Here it simply returns the scanner position. """
		
		return self.scanner.position()
	

	def match(self,token):
		""" Consumes (matches with current lookahead) an expected token.
		Raises ParseError if anything else is found. Acquires new lookahead. """ 
		
		if self.la==token:
			self.la,self.val = self.next_token()
		else:
			raise ParseError("found {} instead of {}".format(self.la,token))
	
	
	def parse(self,fp):
		""" Creates scanner for input file object fp and calls the parse logic code. """
		
		# create the plex scanner for fp
		self.create_scanner(fp)
		
		# call parsing logic
		self.session()
	
			
	def session(self):
		""" Session  -> Facts Question | ( Session ) Session """
		if self.la == "Identifier":
			print("Got identifier")
			self.match(self.la)
			self.equalSign()
		elif self.la == "print":
			print("Got 'print'")
			self.match(self.la)
		
		else:
			raise ParseError("Expected identifier or print keyword")

	def logical(self):
		if self.la == "Got a NOT" or (self.la == "Got an OR" or self.la == "Got an AND"):
			print("found logical")
			self.match(self.la)
			self.identifier()
		else:
			raise ParseError("Expected not, and, or")
		
	
	def identifier(self):
		if self.la == "Identifier":
			print("found Identifier")
			self.match(self.la)
			self.logical()
		elif self.la == "Got a TRUE" or self.la == "Got a FALSE":
			print("found boolean Value")
			self.match(self.la)
			self.logical()
		else:
			raise ParseError("Expected identifier or boolean")

	def equalSign(self):
		if self.la == "equalSign":
			print("found Equal_Sign")
			self.match(self.la)
			self.identifier()
		else:
			raise ParseError("Expected '=' ")
	

# the main part of prog

# create the parser object
parser = MyParser()

# open file for parsing
with open("recursive.txt","r") as fp:

	# parse file
	try:
		parser.parse(fp)
	except errors.PlexError:
		_,lineno,charno = parser.position()	
		print("Scanner Error: at line {} char {}".format(lineno,charno+1))
	except ParseError as perr:
		_,lineno,charno = parser.position()	
		print("Parser Error: {} at line {} char {}".format(perr,lineno,charno+1))
