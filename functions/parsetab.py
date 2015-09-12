
# parsetab.py
# This file is automatically generated. Do not edit.
_tabversion = '3.5'

_lr_method = 'LALR'

_lr_signature = 'A8D4A8C28445D93665848C5283C53450'
    
_lr_action_items = {'COMMA':([8,],[11,]),'NOTEQUAL':([19,],[22,]),'NUMBER':([22,23,24,25,],[29,30,32,33,]),'FROM':([6,7,8,14,],[9,10,-8,-7,]),'AND':([18,26,27,28,29,30,31,32,33,],[20,20,20,-16,-17,-14,-13,-12,-15,]),'EQUAL':([19,],[24,]),'$end':([1,4,],[0,-1,]),'WHERE':([12,13,],[16,16,]),'LESSTHAN':([19,],[23,]),'STRING':([22,24,],[28,31,]),'SEMICOLON':([2,5,12,13,15,17,18,26,27,28,29,30,31,32,33,],[4,-2,-4,-3,-6,-5,-9,-10,-11,-16,-17,-14,-13,-12,-15,]),'OR':([18,26,27,28,29,30,31,32,33,],[21,21,21,-16,-17,-14,-13,-12,-15,]),'IDENTIFIER':([3,9,10,11,16,20,21,],[8,12,13,8,19,19,19,]),'ASTERISK':([3,],[7,]),'SELECT':([0,],[3,]),'GREATERTHAN':([19,],[25,]),}

_lr_action = {}
for _k, _v in _lr_action_items.items():
   for _x,_y in zip(_v[0],_v[1]):
      if not _x in _lr_action:  _lr_action[_x] = {}
      _lr_action[_x][_k] = _y
del _lr_action_items

_lr_goto_items = {'expression':([16,20,21,],[18,26,27,]),'where_statement':([12,13,],[15,17,]),'select_statement':([3,],[5,]),'program':([0,],[1,]),'columns':([3,11,],[6,14,]),'statement':([0,],[2,]),}

_lr_goto = {}
for _k, _v in _lr_goto_items.items():
   for _x, _y in zip(_v[0], _v[1]):
       if not _x in _lr_goto: _lr_goto[_x] = {}
       _lr_goto[_x][_k] = _y
del _lr_goto_items
_lr_productions = [
  ("S' -> program","S'",1,None,None,None),
  ('program -> statement SEMICOLON','program',2,'p_program','parser.py',12),
  ('statement -> SELECT select_statement','statement',2,'p_statement','parser.py',15),
  ('select_statement -> ASTERISK FROM IDENTIFIER','select_statement',3,'p_select_statement','parser.py',21),
  ('select_statement -> columns FROM IDENTIFIER','select_statement',3,'p_select_statement','parser.py',22),
  ('select_statement -> ASTERISK FROM IDENTIFIER where_statement','select_statement',4,'p_select_statement','parser.py',23),
  ('select_statement -> columns FROM IDENTIFIER where_statement','select_statement',4,'p_select_statement','parser.py',24),
  ('columns -> IDENTIFIER COMMA columns','columns',3,'p_columns','parser.py',35),
  ('columns -> IDENTIFIER','columns',1,'p_columns','parser.py',36),
  ('where_statement -> WHERE expression','where_statement',2,'p_where_statement','parser.py',42),
  ('expression -> expression AND expression','expression',3,'p_expression','parser.py',46),
  ('expression -> expression OR expression','expression',3,'p_expression','parser.py',47),
  ('expression -> IDENTIFIER EQUAL NUMBER','expression',3,'p_expression','parser.py',48),
  ('expression -> IDENTIFIER EQUAL STRING','expression',3,'p_expression','parser.py',49),
  ('expression -> IDENTIFIER LESSTHAN NUMBER','expression',3,'p_expression','parser.py',50),
  ('expression -> IDENTIFIER GREATERTHAN NUMBER','expression',3,'p_expression','parser.py',51),
  ('expression -> IDENTIFIER NOTEQUAL STRING','expression',3,'p_expression','parser.py',52),
  ('expression -> IDENTIFIER NOTEQUAL NUMBER','expression',3,'p_expression','parser.py',53),
]