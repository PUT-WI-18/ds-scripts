#include <iostream>
#include <set>
#include <map>
#include <vector>
#include <string>
#include <utility>
#include <algorithm>
#include <cmath>
#include <bitset>
#include <limits>
 
/*
// 1. przykład z ćwiczeń
6
2
8 4 P
5 7 P
2 3 P
5 7 R
2 5 S
8 5 S
 
// 2. przykład z ćwiczeń
7
3
a 1 + B
a 3 - A
a 2 + A
b 1 - B
a 2 + A
b 3 + B
a 1 + A
*/
 
using namespace std;
 
struct X
{
    map<string, map<vector<string>, int>> przyblizeniaDolne;
    map<string, map<vector<string>, int>> przyblizeniaGorne;
    map<string, map<vector<string>, int>> obszaryBrzegowe;
    map<string, string> dokladnosci;
    map<string, string> jakosci;
    string jakoscKlasyfikacji;
};
 
int suma(const map<vector<string>, int> &m)
{
    int r = 0;
    for (const auto &x : m)
        r += x.second;
    return r;
}
 
X policzPrzyblizenia(const map<vector<string>, map<string, int>> &wariantNaKlase, const map<string, int> &klasy)
{
    X x;
    int u = 0, s = 0;
    for (const auto &_klasa : klasy)
    {
        const auto &klasa = _klasa.first;
        x.przyblizeniaDolne[klasa] = {};
        x.przyblizeniaGorne[klasa] = {};
        for (const auto &w : wariantNaKlase)
        {
            if (w.second.count(klasa) > 0)
            {
                if (w.second.size() == 1)
                    for (size_t i = 0; i < w.second.at(klasa); i++)
                        x.przyblizeniaDolne[klasa][w.first]++;
 
                for (const auto &klasyWariantu : w.second)
                    for (size_t i = 0; i < klasyWariantu.second; i++)
                        x.przyblizeniaGorne[klasa][w.first]++;
            }
        }
        x.obszaryBrzegowe[klasa] = x.przyblizeniaGorne[klasa];
        for (const auto &przyblizenieDolne : x.przyblizeniaDolne[klasa])
            x.obszaryBrzegowe[klasa][przyblizenieDolne.first] -= przyblizenieDolne.second;
        x.dokladnosci[klasa] = to_string(suma(x.przyblizeniaDolne[klasa])) + "/" + to_string(suma(x.przyblizeniaGorne[klasa]));
        x.jakosci[klasa] = to_string(suma(x.przyblizeniaDolne[klasa])) + "/" + to_string(_klasa.second);
        u += _klasa.second;
        s += suma(x.przyblizeniaDolne[klasa]);
    }
    x.jakoscKlasyfikacji = to_string(s) + "/" + to_string(u);
    return x;
}
 
using bits = int8_t;
 
vector<bits> policzRedukty(const string &jakoscKlasyfikacji, const map<vector<string>, map<string, int>> &wariantNaKlase, const map<string, int> &klasy)
{
    bits max = 1 << wariantNaKlase.begin()->first.size();
    vector<bits> redukty;
    for (bits i = 0; i < max; i++)
    {
        map<vector<string>, map<string, int>> wariantNaKlaseR;
        for (const auto &w : wariantNaKlase)
        {
            bits t = i;
            vector<string> v;
            for (int j = 0; j < w.first.size() && t; j++)
            {
                if (t & 1)
                    v.push_back(w.first[j]);
                t >>= 1;
            }
            for (const auto &klasyWariantu : w.second)
                wariantNaKlaseR[v][klasyWariantu.first] += klasyWariantu.second;
        }
 
        X x = policzPrzyblizenia(wariantNaKlaseR, klasy);
        if (x.jakoscKlasyfikacji == jakoscKlasyfikacji)
            redukty.push_back(i);
    }
 
    auto kopia = redukty;
 
    for (const auto &k : kopia)
    {
        auto it = redukty.begin();
        while (it != redukty.end())
        {
            if ((*it & k) == k && *it != k)
                it = redukty.erase(it);
            else
                ++it;
        }
    }
 
    return redukty;
}
 
void wypiszRedukt(bits redukt)
{
    std::bitset<sizeof(bits) * 8> b(redukt);
    string temp = b.to_string('_', 'X');
    cout << string(temp.rbegin(), temp.rend());
}
 
void wypiszRedukty(vector<bits> redukty)
{
    cout << "Redukty:\n  12345...\n";
    bits rdzen = numeric_limits<bits>::max();
    for (const auto &redukt : redukty)
    {
        cout << "  ";
        wypiszRedukt(redukt);
        cout << '\n';
        rdzen = rdzen & redukt;
    }
    cout << "Rdzen:\n";
    cout << "  ";
    wypiszRedukt(rdzen);
    cout << '\n';
}
 
void wypiszZbior(const map<vector<string>, int> &zbior)
{
    for (const auto &element : zbior)
        for (size_t i = 0; i < element.second; i++)
        {
            cout << "    ";
            for (const auto &atrybut : element.first)
                cout << atrybut << ' ';
            cout << '\n';
        }
}
 
void wypiszPrzyblizenia(const X &x, const map<string, int> &klasy)
{
    cout << "Jakosc klasyfikacji yp(Cl): " << x.jakoscKlasyfikacji << '\n';
    for (const auto &_klasa : klasy)
    {
        const auto &klasa = _klasa.first;
        cout << "Klasa: " << klasa << '\n';
        cout << "  Dolne przyblizenie P_(" << klasa << "):\n";
        wypiszZbior(x.przyblizeniaDolne.at(klasa));
        cout << "  Gorne przyblizenie P^(" << klasa << "):\n";
        wypiszZbior(x.przyblizeniaGorne.at(klasa));
        cout << "  Obszar brzegowy Bnp(" << klasa << "):\n";
        wypiszZbior(x.obszaryBrzegowe.at(klasa));
        cout << "  Dokladnosc ap(" << klasa << "): " << x.dokladnosci.at(klasa) << '\n';
        cout << "  Jakosc yp(" << klasa << "): " << x.jakosci.at(klasa) << '\n';
    }
}
 
int main()
{
    int u, n;
    map<vector<string>, map<string, int>> wariantNaKlase;
    map<string, int> klasy;
    cin >> u >> n;
    for (size_t i = 0; i < u; i++)
    {
        vector<string> atrybuty(n);
        string klasa;
        for (auto &atrybut : atrybuty)
            cin >> atrybut;
        cin >> klasa;
        wariantNaKlase[atrybuty][klasa]++;
        klasy[klasa]++;
    }
    X x = policzPrzyblizenia(wariantNaKlase, klasy);
    wypiszPrzyblizenia(x, klasy);
    vector<bits> redukty = policzRedukty(x.jakoscKlasyfikacji, wariantNaKlase, klasy);
    wypiszRedukty(redukty);
 
    return 0;
}