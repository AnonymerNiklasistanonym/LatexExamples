#include <iostream>

class NumberArray {
private:
    int* arr;       // pointer to dynamic array
    int size;

public:
    // Constructor: allocate and initialize array
    NumberArray(int n = 10) {  // default size 10
        size = n;
        arr = new int[size];
        for (int i = 0; i < size; i++) {
            arr[i] = i + 1; // initialize with 1,2,...,size
        }
        std::cout << "Constructor: Array of size " << size << " created." << std::endl;
    }

    // Destructor: free allocated memory
    ~NumberArray() {
        delete[] arr;
        std::cout << "Destructor: Array memory released." << std::endl;
    }

    // Method to print array
    void print() const {
        for (int i = 0; i < size; i++) {
            std::cout << arr[i] << " ";
        }
        std::cout << std::endl;
    }
};

int main() {
    std::cout << "Creating NumberArray object..." << std::endl;
    NumberArray numbers;  // default size 10

    numbers.print();

    std::cout << "Exiting main function..." << std::endl;
    // Destructor automatically called here
    return 0;
}