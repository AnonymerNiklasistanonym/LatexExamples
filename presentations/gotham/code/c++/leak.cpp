void leak() {
    int* data = new int[10];  // allocated
    data[0] = 42;
    // missing delete[] → leak
}
int main() {
    leak();
}
