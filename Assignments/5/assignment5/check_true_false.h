#include <vector>

using namespace std;

class logical_expression	
{  
public:
	char symbol[20]; // null if sentence is a more complex expression
	char connective[20]; // null if sentice is a symbol
	vector<logical_expression *> subexpressions;

	logical_expression();
	~logical_expression();
};


void print_expression(logical_expression * expression, char * separator);

logical_expression * read_expression(char * input_string);
logical_expression * read_expression(char * input_string, long & counter);

long read_subexpressions(char * input_string, long & counter, 
                         vector <logical_expression*> & subexpressions);

void read_word(char * input_string, long & counter, char * connective);
long valid_expression(logical_expression * expression);
long valid_symbol(char * symbol);
int exit_function(int value);

void check_true_false(logical_expression * knowledge_base, 
                      logical_expression * statement);




