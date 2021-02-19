#include <iostream>
#include <vector>
#include <algorithm>


using namespace std;

bool checkCertainRule(vector<string> arr, string rule) {

	//conditions number
	cout << "Sprawdzanie czy regula " << rule << " jest regula pewna" << endl;
	bool same = true;
	for (size_t i = 0; i < arr.size(); i++) {
		same = true;
		for (size_t j = 0; j < arr[i].size() - 1; j++) {
			if (arr[i][j] != rule[j] && rule[j] != '_') {
				same = false;
				break;
			}
		}
		if (same && arr[i][arr[i].size() - 1] != rule[arr[i].size() - 1]) {
			cout << "Nie jest to regula pewna!" << endl;
			return false;
		}
	}
	cout << "To jest regula pewna! " << endl;
	return true;
}

vector<string> comb(int N, int K, string rule) {
	string bitmask(K, 1);
	bitmask.resize(N, 0);
	vector<string> result;
	do {
		string r(rule.size(), '_');
		r[rule.size() - 1] = rule[rule.size() - 1];
		for (int i = 0; i < N; ++i)
		{
			int t = -1;
			int j = 0;
			if (bitmask[i]) {
				while (t != i) {
					if (rule[j] != '_') {
						t++;
					}
					j++;
				}
				r[j-1] = rule[j-1];
			}
		}
		result.push_back(r);
	} while (prev_permutation(bitmask.begin(), bitmask.end()));
	return result;
}



bool checkCertainMinimalRule(vector<string> arr, string rule) {
	int nCon = 0;
	for (size_t i = 0; i < rule.size() - 1; i++) {
		if (rule[i] != '_') {
			nCon++;
		}
	}
	if (checkCertainRule(arr, rule)) {
		for (int i = 1; i < nCon; i++) {
			vector<string> combinations = comb(nCon, i, rule);
			for (size_t j = 0; j < combinations.size(); j++) {
				if (checkCertainRule(arr, combinations[j])) {
					cout << "Regula " << combinations[j] << " jest regula pewna, co oznacza, ze regula " << rule << " nie jest minimalna!" << endl;
					return false;
				}
			}
		}
	}
	else {
		return false;
	}
	return true;
}



int main() {
	int objects, attributes;
	cout << "Wprowadz liczbe obiektow: ";
	cin >> objects;
	cout << "Wprowadz liczbe atrybutow(z DEC wlacznie): ";
	cin >> attributes;
	vector<string> arr(objects);
	int i = 0;
	cout << "Atrybuty(od A do DEC) prosze wprowadzac bez spacji jako jeden ciag znakow" << endl;
	for (auto& s : arr) {
		char letter = 97 + i;
		cout << "Wprowadz atrybuty obiektu nr " << i++ << "("<< letter << "): ";
		cin >> s;
		if ((int)s.size() != attributes) {
			cout << "Nieprawidlowa ilosc atrybutow! Koniec programu!" << endl;
			return 0;
		}
	}
	string rule;
	cout << "Przyklad reguly: If A=2 and C=2 then Y | w programie dla 4 atrybutow: 2_2_Y\nPodaj regule do sprawdzenia: ";
	cin >> rule;
	if (checkCertainMinimalRule(arr, rule)) {
		cout << endl << "Regula " << rule << " jest minimalna pewna regula!" << endl;
	}
	else {
		cout << endl << "Regula " << rule << " nie jest minimalna pewna regula!" << endl;
	}
	return 0;
}
