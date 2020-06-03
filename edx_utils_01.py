import numpy as np

####################################################################
# Used if running this python code outside MOOC test platform
#
if not 'anonymous_student_id' in globals().keys():
  anonymous_student_id = 'student'

####################################################################
# init numpy random generator
#
def InitRandomGenerator( problem_id = '' ):
    maxint = np.iinfo(np.int32).max
    rnd_seed = hash( str( anonymous_student_id ) \
                   + str(problem_id) ) % maxint
    np.random.seed( rnd_seed )

####################################################################
# Uses the random number generator of numpy
# This function should be used instead of random.choice()
#
def RandomPick( lst ):
  return lst[ np.random.randint( 0, len( lst ) ) ]

####################################################################
# Creates num_entries-1 invalid answers such that
#
# This function generates the global variables associated with
#  $a_answer_0,..., $a_answer_4 and
#  $a_value_0,..., $a_value_4 and
#
#  <multiplechoiceresponse>
#    <choicegroup type="MultipleChoice">
#      <choice correct="$a_answer_0" > $a_value_0 </choice>
#      <choice correct="$a_answer_1" > $a_value_1 </choice>
#      <choice correct="$a_answer_2" > $a_value_2 </choice>
#      <choice correct="$a_answer_3" > $a_value_3 </choice>
#      <choice correct="$a_answer_4" > $a_value_4 </choice>
#    </choicegroup>
#  </multiplechoiceresponse>
#
# prefix - the '*' used in the variables *_answer_0 and *_value_0
# value - correct answer
# ndigs - digits after the comma
# suffix - usually the units of values
# entries - total number of displayed values
# delta - absolute value of the desired mean interval between values
# limits - 'greater', 'smaller', 'both'
#
def NumericMultipleChoice( prefix, value, ndigs, suffix, entries, gdelta, 
                             limits = 'both' ):

    def fmt_val( val, dig ):
        return "{vl:.{dg}f}".format( vl = val, dg = dig )

    # number of wrong answers
    num_err = entries-1

    # generate a set of equally spaced undisturbed values
    low_up = { 'greater': ( 1, entries ), 
               'less'   : ( -num_err, 0 ), 
               'both'   : ( -num_err, entries ) }
    lw, up = low_up[ limits ]
    
    delta = gdelta / ( 2*num_err if limits == 'both' else num_err ) 
    options = [ [ "false", i*delta + value ] for i in range(lw,up) if i != 0 ]

    # shuffle and pick num_err entries
    np.random.shuffle(options)
    options = options[0:num_err]

    # disturb the set of wrong answers
    fdelta = delta * 0.40 # maximum perturbation
    for opt in options:
        ss = -1.0 if np.random.uniform() < 0.5 else +1.0
        opt[1] += ss * fdelta * np.random.uniform()

    # append the correct answer and shuffle
    options.append( [ "true",  value ] )
    np.random.shuffle(options)
    
    # set the global variables
    gdic = globals()
    for i, opt in enumerate( options ):
        gdic[ '%s_answer_%i' % (prefix,i) ] = opt[0]
        gdic[ '%s_value_%i'  % (prefix,i) ] = fmt_val( opt[1], ndigs ) + ' ' + suffix

####################################################################
# Shuffles all the answers and generates the global variables 
# associated with
#  $a_answer_0,..., $a_answer_4 and
#  $a_value_0,..., $a_value_4 and
#
#  <multiplechoiceresponse>
#    <choicegroup type="MultipleChoice">
#      <choice correct="$a_answer_0" > $a_value_0 </choice>
#      <choice correct="$a_answer_1" > $a_value_1 </choice>
#      <choice correct="$a_answer_2" > $a_value_2 </choice>
#      <choice correct="$a_answer_3" > $a_value_3 </choice>
#      <choice correct="$a_answer_4" > $a_value_4 </choice>
#    </choicegroup>
#  </multiplechoiceresponse>
#
#-------------------------------------------------------------------
# Parameters:
#
# prefix - the '*' used in the variables *_answer_0 and *_value_0
# correct: string with the correct answer   
# wrong_lst: list of string with wrong answers
#
def StringMultipleChoice( prefix, shuffle_lst, fixed_lst=None ):

    # shuffle and pick num_err entries
    options = list( shuffle_lst ) 
    np.random.shuffle( options )
    if fixed_lst != None:
      options += list( fixed_lst )
    
    # set the global variables
    gdic = globals()
    for i, opt in enumerate( options ):
        gdic[ '%s_answer_%i' % (prefix,i)  ] = opt[0]
        gdic[ '%s_value_%i'  % (prefix,i)  ] = opt[1]

####################################################################
####################################################################
####################################################################