#include <iostream>
#include <cmath>

using namespace std;

int main() {
    float xa, ya;
    float xb, yb;
    float xc, yc;

    cout << "Enter coordinates of point A (x y): ";
    cin >> xa >> ya;

    cout << "Enter coordinates of point B (x y): ";
    cin >> xb >> yb;

    cout << "Enter coordinates of point C (x y): ";
    cin >> xc >> yc;

    float AB = sqrt(pow(xb - xa, 2) + pow(yb - ya, 2));
    float BC = sqrt(pow(xc - xb, 2) + pow(yc - yb, 2));
    float AC = sqrt(pow(xc - xa, 2) + pow(yc - ya, 2));

    float perimeter = AB + BC + AC;
    float p = perimeter / 2;
    float area = sqrt(p * (p - AB) * (p - BC) * (p - AC));

    cout << "\nTriangle perimeter: " << perimeter << endl;
    cout << "Triangle area: " << area << endl;

    cout << "\nPress Enter to exit...";
    cin.ignore();
    cin.get();

    return 0;
}
