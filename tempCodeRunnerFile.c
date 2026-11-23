#include <iostream.h>
#include <conio.h>
#include <string.h>

// Node Structure
class Node {
public:
    char location[50]; // Using char array for older C++ compatibility
    Node* next;
    Node* prev;

    Node(char loc[]) {
        strcpy(location, loc);
        next = NULL;
        prev = NULL;
    }
};

// Circular Doubly Linked List Class
class GISCircularDoublyLinkedList {
private:
    Node* head;

public:
    GISCircularDoublyLinkedList() {
        head = NULL;
    }

    // Insert a new location
    void insert_location(char location[]) {
        Node* new_node = new Node(location);
        if (head == NULL) {
            head = new_node;
            new_node->next = head;
            new_node->prev = head;
        } else {
            Node* last = head->prev;
            new_node->next = head;
            new_node->prev = last;
            last->next = new_node;
            head->prev = new_node;
        }
        cout << "Location '" << location << "' added successfully.\n";
    }

    // Display locations in forward direction
    void display_forward() {
        if (head == NULL) {
            cout << "No GIS locations available.\n";
            return;
        }
        cout << "\nGIS Locations (Forward Traversal):\n";
        Node* temp = head;
        do {
            cout << temp->location << " -> ";
            temp = temp->next;
        } while (temp != head);
        cout << "(Head)\n";
    }

    // Display locations in backward direction
    void display_backward() {
        if (head == NULL) {
            cout << "No GIS locations available.\n";
            return;
        }
        cout << "\nGIS Locations (Backward Traversal):\n";
        Node* temp = head->prev;
        Node* last = head->prev;
        do {
            cout << temp->location << " -> ";
            temp = temp->prev;
        } while (temp != last);
        cout << "(Last)\n";
    }

    // Search a location
    void search_location(char location[]) {
        if (head == NULL) {
            cout << "GIS database is empty.\n";
            return;
        }
        Node* temp = head;
        do {
            if (strcmp(temp->location, location) == 0) {
                cout << "Location '" << location << "' found.\n";
                return;
            }
            temp = temp->next;
        } while (temp != head);
        cout << "Location '" << location << "' not found.\n";
    }

    // Count total locations
    int count_locations() {
        if (head == NULL) {
            return 0;
        }
        int count = 0;
        Node* temp = head;
        do {
            count++;
            temp = temp->next;
        } while (temp != head);
        return count;
    }
};

// Main Program
void main() {
    clrscr(); // Clear screen for Turbo C++

    GISCircularDoublyLinkedList gis;

    // Insert Locations
    gis.insert_location("Madurai");
    gis.insert_location("Chennai");
    gis.insert_location("Coimbatore");
    gis.insert_location("Trichy");
    gis.insert_location("Salem");

    // Display Data
    gis.display_forward();
    gis.display_backward();

    // Search Operation
    gis.search_location("Chennai");

    // Count Locations
    cout << "\nTotal GIS Locations: " << gis.count_locations() << "\n";

    getch(); // Hold the output screen in Turbo C++
}