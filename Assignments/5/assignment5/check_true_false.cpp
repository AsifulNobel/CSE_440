#include <stdio.h>
#include <ctype.h>
#define string_length strlen

#include "check_true_false.h"



logical_expression::logical_expression()
{
  symbol[0] = 0;
  connective[0] = 0;
}


logical_expression::~logical_expression()
{
  unsigned long counter;
  for (counter = 0; counter < subexpressions.size(); counter++)
  {
    delete subexpressions[counter];
  }
}


void print_expression(logical_expression * expression, char * separator)
{
  if (expression == 0)
  {
    printf("\nINVALID\n");
  }
  else if (strcmp(expression->symbol, "") != 0)
  {
    printf("%s", expression->symbol);
  }
  else
  {
    printf("(%s",  expression->connective);
    unsigned long counter;
    for (counter = 0; counter < expression->subexpressions.size(); counter++)
    {
      printf(" ");
      print_expression(expression->subexpressions[counter], "");
      printf(separator);
    }
    printf(")");
  }
}


logical_expression * read_expression(char * input_string)
{
  long counter = 0;
  return read_expression(input_string, counter);
}


logical_expression * read_expression(char * input_string, long & counter)
{
  logical_expression * result = new logical_expression();
  long length =  string_length(input_string);
  while(1)
  {
    if (counter >= length)
    {
      break;
    }
    if (isspace(input_string[counter]))    // skip whitespace
    {
      counter++;
      continue;
    }
    else if (input_string[counter] == '(')
    {
      counter++;
      read_word(input_string, counter, result->connective);
      read_subexpressions(input_string, counter, result->subexpressions);
      break;
    }
    else
    {
      read_word(input_string, counter, result->symbol);
      break;
    }
  }

  return result;
}


long read_subexpressions(char * input_string, long & counter, 
                         vector <logical_expression*> & subexpressions)
{
  long length =  string_length(input_string);
  while(1)
  {
    if (counter >= length)
    {
      printf("\nunexpected end of input\n");
      return 0;
    }
    if (isspace(input_string[counter]))    // skip whitespace
    {
      counter++;
      continue;
    }
    if (input_string[counter] == ')') // we are done
    {
      counter++;
      return 1;
    }
    else
    {
      logical_expression * expression = read_expression(input_string, counter);
      subexpressions.push_back(expression);
    }
  }
}


void read_word(char * input_string, long & counter, char * target)
{
  unsigned long second_counter = 0;
  while (1)
  {
    if (counter >= (long) string_length(input_string))
    {
      break;
    }
    if ((isalpha(input_string[counter])) || (input_string[counter] == '_') ||
        (isdigit(input_string[counter])))
    {
      target[second_counter] = input_string[counter];
      counter++;
      second_counter++;
    }
    else if ((input_string[counter] == ')') || (isspace(input_string[counter])))
    {
      break;
    }
    else
    {
      printf("unexpected character %c\n", input_string[counter]);
      exit_function(0);
    } 
  }

  target[second_counter] = 0;
}


long valid_expression(logical_expression *  expression)
{
  if (strcmp(expression->symbol, "") != 0)
  {
    return valid_symbol(expression->symbol);
  }

  if ((strcasecmp(expression->connective, "if") == 0) ||
      (strcasecmp(expression->connective, "iff") == 0))
  {
    if (expression->subexpressions.size() != 2)
    {
      printf("error: connective \"%s\" with %li arguments\n", 
             expression->connective, expression->subexpressions.size());
      return 0;
      return 0;
    }
  }
  else   if (strcasecmp(expression->connective, "not") == 0)
  {
    if (expression->subexpressions.size() != 1)
    {
      printf("error: connective \"%s\" with %li arguments\n", 
             expression->connective, expression->subexpressions.size());
      return 0;
    }
  }
  else if ((strcasecmp(expression->connective, "and") != 0) &&
           (strcasecmp(expression->connective, "or") != 0) &&
           (strcasecmp(expression->connective, "xor") != 0))
  {
    printf("error: unknown connective %s\n", expression->connective);
    return 0;
  }

  unsigned long counter;
  for (counter = 0; counter < expression->subexpressions.size(); counter++)
  {
    if (valid_expression(expression->subexpressions[counter]) == 0)
    {
      return 0;
    }
  }

  return 1;
}


long valid_symbol(char * symbol)
{
  if ((symbol == 0) || (strlen(symbol) == 0))
  {
    return 0;
  }
  unsigned long counter;
  for (counter = 0; counter < strlen(symbol);  counter++)
  {
    if ((symbol[counter] != '_') && (! (isalpha(symbol[counter]))) && (! (isdigit(symbol[counter]))))
    {
      return 0;
    }       
  }

  return 1;
}


int exit_function(int value)
{
//	char str_buf[200]; 
//	printf("Press <ENTER> to exit.\n");
//	gets(str_buf);

  exit(value);
  return value;
}


void check_true_false(logical_expression * knowledge_base, 
                      logical_expression * statement)
{
  // your code goes here
  printf("\nI don't know if the statement is definitely true or definitely false.\n");

  FILE * fp = fopen("result.txt", "wb");
  if (fp == 0)
  {
    printf("something is wrong, cannot open result.txt for writing\n");
  }
  else
  {
    fprintf(fp, "result unknown");
    fclose(fp);
  }
}


int main(int argc, char ** argv)
{
  char ** command_line = argv;
  if(argc != 4) 
  {
  // take two arguments
    printf("Usage: %s [wumpus-rules-file] [additional-knowledge-file] [input_file]\n", command_line [0]);
    return exit_function(0);
  }

  char buffer[200];
  char * input;
  FILE * input_file;

  // read wumpus rules
  input = command_line[1];
  input_file = fopen(input, "rb");
  if (input_file == 0)
  {
    printf("failed to open file %s\n", input);
    return exit_function(0);
  }

  printf("Loading wumpus rules...\n");
  logical_expression * knowledge_base = new logical_expression();
  strcpy(knowledge_base->connective, "and");
  while(fgets(buffer, 200, input_file) != NULL)
  {
    // skip lines starting with # (comment lines), or empty lines
    if ((buffer[0] == '#') || (buffer[0] == 0) || (buffer[0] == 13) || (buffer[0] == 10))
    {
      continue;
    }
    logical_expression * subexpression = read_expression(buffer);
    knowledge_base->subexpressions.push_back(subexpression);
  }
  fclose(input_file);
  
  // read additional knowledge
  input = command_line[2];
  input_file = fopen(input, "rb");
  if (input_file == 0)
  {
    printf("failed to open file %s\n", input);
    return exit_function(0);
  }

  printf("Loading additional knowledge...\n");
  while(fgets(buffer, 200, input_file) != NULL)
  {
    // skip lines starting with # (comment lines), or empty lines
    if ((buffer[0] == '#') || (buffer[0] == 0) || (buffer[0] == 13) || (buffer[0] == 10))
    {
      continue;
    }
    logical_expression * subexpression = read_expression(buffer);
    knowledge_base->subexpressions.push_back(subexpression);
  }
  fclose(input_file);
  
  if (valid_expression(knowledge_base) == 0)
  {
    printf("invalid knowledge base\n");
    return exit_function(0);
  }

  print_expression(knowledge_base, "\n");

  // read statement whose entailment we want to determine.
  input = command_line[3];
  input_file = fopen(input, "rb");
  if (input_file == 0)
  {
    printf("failed to open file %s\n", input);
    return exit_function(0);
  }

  printf("\n\nLoading statement...\n");
  fgets(buffer, 200, input_file);
  fclose(input_file);

  logical_expression * statement = read_expression(buffer);
  if (valid_expression(statement) == 0)
  {
    printf("invalid statement\n");
    return exit_function(0);
  }

  print_expression(statement, "");

  check_true_false(knowledge_base, statement);

  delete knowledge_base;
  delete statement;
  exit_function(1);
}
