#include "sort.h"

/**
 * cocktail_sort_list - cocktail sort function
 * @list: list
 */

void cocktail_sort_list(listint_t **list)
{
	int swapped;
	listint_t *start = *list;
	listint_t *end = NULL;

	if (!list || !(*list))
		return;

	do
	{
		swapped = 0;

		for (; start->next != end; start = start->next)
		{
			if (start->n > start->next->n)
			{
				swap_nodes(list, start, start->next);
				swapped = 1;
			}
		}
		end = start;

		for (; start->prev != NULL; start = start->prev)
		{
			if (start->n < strat->prev->n)
			{
				swap_nodes(list, start->prev->n, start);
				swapped = 1;
			}
		}
	}
	while (swapped);
	print_list(*list);
}
