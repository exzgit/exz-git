#include <iostream>
#include <string>

class Bunga {
public:
    std::string nama;
    std::string warna;
    bool hidup;

    void Berbunga() {
        if (hidup) {
            std::cout << "Bunga " << nama << " sedang mekar dengan warna " << warna << "." << std::endl;
        } else {
            std::cout << "Bunga " << nama << " sudah mati." << std::endl;
        }
    }
};

int main() {
    // Buat objek Bunga bernama mawar
    Bunga mawar;

    // Isi atribut objek
    mawar.nama = "Mawar";
    mawar.warna = "merah";
    mawar.hidup = true;

    // Panggil method Berbunga pada objek mawar ketika masih hidup
    mawar.Berbunga();

    // Mengubah kondisi hidup menjadi mati
    mawar.hidup = false;

    // Panggil method Berbunga pada objek mawar setelah bunga mati
    mawar.Berbunga();

    return 0;
}
