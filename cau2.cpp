
#include <iostream>
#include <stack>
#include <string>
#include <cctype>
using namespace std;

// Hàm trả độ ưu tiên của toán tử
int doUuTien(char op) {
    if (op == '^') return 3;
    if (op == '*' || op == '/') return 2;
    if (op == '+' || op == '-') return 1;
    return 0;
}

// Hàm kiểm tra xem ký tự có phải là toán tử
bool laToanTu(char c) {
    return c == '+' || c == '-' || c == '*' || c == '/' || c == '^';
}

// Chuyển infix sang postfix
string infix_To_Postfix(string infix) {
    stack<char> st;
    string postfix = "";

    for (int i = 0; i < infix.length(); i++) {
        char c = infix[i];

        // Bỏ qua khoảng trắng
        if (c == ' ') continue;

        // Nếu là số (hoặc chuỗi nhiều chữ số)
        if (isdigit(c)) {
            while (i < infix.length() && (isdigit(infix[i]) || infix[i] == '.')) {
                postfix += infix[i];
                i++;
            }
            postfix += " ";
            i--; // Tránh bỏ qua ký tự tiếp theo
        }

        // Nếu là dấu mở ngoặc
        else if (c == '(') {
            st.push(c);
        }

        // Nếu là dấu đóng ngoặc
        else if (c == ')') {
            while (!st.empty() && st.top() != '(') {
                postfix += st.top(); postfix += " ";
                st.pop();
            }
            if (!st.empty() && st.top() == '(')
                st.pop(); // Bỏ dấu (
        }

        // Nếu là toán tử
        else if (laToanTu(c)) {
            while (!st.empty() && doUuTien(c) <= doUuTien(st.top())) {
                postfix += st.top(); postfix += " ";
                st.pop();
            }
            st.push(c);
        }
    }

    // Đẩy các toán tử còn lại trong stack ra
    while (!st.empty()) {
        postfix += st.top(); postfix += " ";
        st.pop();
    }

    return postfix;
}

int main() {
    string infix;
	cout<<"Bieu thuc trung to la:"<<endl;
	getline(cin,infix);
//	"3 + 5 ^ ( 12 / 6 + 1 ) - 7 * 15 / 3 + 6";
    string postfix = infix_To_Postfix(infix);
    cout<<endl;
    cout << "Bieu thuc hau to la:\n" << postfix << endl;
    return 0;
}
