# This is a sample Python script.
import generator
# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')
    edges = generator.gen_graph(5,10)
    generator.open_write_to_file(edges)
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
