#include <stdio.h>
#include <stdlib.h>

struct Node{
    int data;
    struct Node *link;
};

void printLinkedList(struct Node* n)
{
    while(n != NULL)
    {
        printf("%d ", n->data);
        n = n->link;
    }
    // printf("%d ", n->data);
}

void main(){
    struct Node* head = NULL;
    struct Node* second = NULL;
    struct Node* third = NULL;

    head = (struct Node*)malloc(sizeof(struct Node));
    second = (struct Node*)malloc(sizeof(struct Node));
    third = (struct Node*)malloc(sizeof(struct Node));

    head->data = 1;
    head->link = second;

    second->data = 2;
    second->link = third;

    third->data = 3;
    third->link = NULL;

    printLinkedList(head);
}

