#ifndef MYLIST
#define MYLIST

#include <Arduino.h>
#include <stdio.h>
#include <stdlib.h>
//#include <string.h>
//#include <err.h>

/*
  Data structure definition for the list items. Each item contains
  some data (in this case just an integer number) and a pointer to
  the next item.
  
  (Do not change this.)
*/
typedef struct item_s {
  String data;
  struct item_s * next;
} Item;


/*
  Data structure definition for the list itself. It contains a pointer
  to the head (first item on the list) and to the tail (last item on
  the list). Keeping a pointer to the tail makes it easier to append
  items to the list.
  
  (Do not change this.)
*/
typedef struct list_s {
  Item * head;
  Item * tail;
} List;


/*
  Function to create an empty list. The memory used by the list has to
  be given back to the system by calling destroy at the end.
  
  (Do not change this.)
*/
List * create (void)
{
  List * list;
  
  list = calloc (1, sizeof *list);
  if (NULL == list) {
    //err (EXIT_FAILURE, "%s: calloc", __func__);
  }
  
  return list;
}


// Clear the list
void clear(List * list)
{
  list = calloc (1, sizeof *list);
  if (NULL == list) {
    //err (EXIT_FAILURE, "%s: calloc", __func__);
  }
}

/*
  Function to append an item to an existing list. It shows an example
  for you to start on the exercises, so make sure you understand what
  it does.
  
  (Do not change this.)
*/
void append (List * list, String data)
{
  Item * item;
  
  /*
    Allocate memory for the new list item which will store the given
    data, check that we got valid memory, and save the user-given data
    in the new item.
  */
  
  item = malloc (sizeof *item);
  if (NULL == item) {
    //err (EXIT_FAILURE, "%s: malloc", __func__);
  }
  item->data = data;
  
  /*
    Set the next pointer of the new item and update the head and tail
    pointers of the list.  Notice that the order of assignments can
    matter a lot here.  It can help to draw a diagram of the items and
    the pointers that need to get changed.
  */
  
  item->next = NULL;
  
  if (NULL == list->head) {
    list->head = item;
    list->tail = item;
  }
  else {
    list->tail->next = item;
    //list->tail = item;
  }
}


/*
  FILL IN THIS FUNCTION FOR EXERCISE 4.1.1
  
  Function to prepend an item to an existing list.  You can write this
  function by copying and adapting the append() function.
*/
void prepend (List * list, String data)
{
     Item *item;
  
 item = malloc (sizeof *item);
 if (NULL == item) {
    //err (EXIT_FAILURE, "%s: malloc", __func__);
  }
  item->data = data;


  if (NULL == list->head) {
    
    list->head = item;
    list->tail = item;
  
  }
  
  else
  {   
    //list->p1 = list->head;
    //list->head = item;
    //list->head->next = list->p1;
    
  }
}


/*
  FILL IN THIS FUNCTION FOR EXERCISE 4.1.2
  
  Function to insert an item into to an existing list, such that the
  new item will come immediately after a given item (called "pos" for
  "position").  You have to be careful about possible special cases,
  for example when the given position is the tail of the list, then
  the tail has to be updated by this function as well.
*/
void ins_after (List * list, Item * pos, String data)
{
}


/*
  FILL IN THIS FUNCTION FOR EXERCISE 4.1.3
  
  Function to remove the first item from a given list.  When the list
  is empty, nothing should be changed.  Remember to call free() on the
  item that is removed, and to adjust the head of the list.
  
  To test this function, you have to modify the main function by
  un-commenting the while loop, as described in the code comments of
  the main function (see below).
*/
void rem_head (List * list)
{
}


/*
  Function to print the contents of a list on one line of text.
  
  (Do not change this.)
*/
void print (List * list)
{
  Item * item;
  if (NULL == list->head) {
    //printf ("  [empty]\n");
    Serial.println("  [empty]\n");
  }
  else {
    //printf (" ");
    Serial.println(" ");
    for (item = list->head; NULL != item; item = item->next) {
      //printf (" %3d", item->data);
      Serial.println(item->data);
    }
    //printf ("   [tail: %3d]\n", list->tail->data);
    Serial.println(list->tail->data);
  }
}


/*
  Function to delete all items of a list as well as the list itself.
  It gives memory back to the system by calling free().
  
  (Do not change this.)
*/
void destroy (List * list)
{
  Item * tmp;
  while (NULL != list->head) {
    tmp = list->head->next;
    free (list->head);
    list->head = tmp;
  }
  free (list);
}


/*
  Main function to test the list operations.  It creates two lists
  from some test data (one list is in the same order as the test data,
  the other in reverse).
  
  Change this function AFTER IMPLEMENTING the rem_head() function in
  exercise 4.1.3 by un-commenting the while loop close to the end of
  the main function.
*/
/*
int main (int argc, char ** argv)
{
  static int const data[] = { 3, 14, 15, 92 };
  int ii;
  List * fwd;
  List * rev;
  
  fwd = create ();
  rev = create ();
  for (ii = 0; ii < sizeof(data)/sizeof(*data); ++ii) {
    append (fwd, data[ii]);
    prepend (rev, data[ii]);
  }
  
  printf ("forward:");
  print (fwd);
  printf ("reverse:");
  print (rev);
  
  ins_after (fwd, fwd->head, -11);
  printf ("ins_after head:    ");
  print (fwd);
  
  ins_after (fwd, fwd->tail, -22);
  printf ("ins_after tail:    ");
  print (fwd);
  
  ins_after (fwd, fwd->head->next, -33);
  printf ("ins_after 2nd item:");
  print (fwd);
  
  // /*
    // UN-COMMENT THIS while loop only after you have implemented the
    // rem_head() function for exercise 4.1.3.
    
  // while (NULL != fwd->head) {
    // rem_head (fwd);
    // printf ("removed head:");
    // print (fwd);
  // }
  // 
  
  destroy (fwd);
  destroy (rev);
  
  return 0;
}
*/
#endif //MYLIST