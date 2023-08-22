using System;
using System.Collections.Generic;

class Barang
{
    public string Nama { get; set; }
    public decimal Harga { get; set; }
    public string Kode { get; set; }
    public int Stock { get; set; }
}

class Program
{
    static List<Barang> daftarBarang = new List<Barang>();

    static void Main(string[] args)
    {
        while (true)
        {
            Console.WriteLine("Menu Sahabat Pecinta Barang:");
            Console.WriteLine("1. Tambah Barang");
            Console.WriteLine("2. Lihat Daftar Barang");
            Console.WriteLine("3. Update Barang");
            Console.WriteLine("4. Hapus Barang");
            Console.WriteLine("5. Keluar");
            Console.Write("Pilihanmu: ");

            if (int.TryParse(Console.ReadLine(), out int pilihan))
            {
                switch (pilihan)
                {
                    case 1:
                        TambahBarang();
                        break;
                    case 2:
                        LihatDaftarBarang();
                        break;
                    case 3:
                        UpdateBarang();
                        break;
                    case 4:
                        HapusBarang();
                        break;
                    case 5:
                        return;
                    default:
                        Console.WriteLine("Pilihanmu nggak jelas. Coba lagi, ya.");
                        break;
                }
            }
            else
            {
                Console.WriteLine("Hayo, kamu salah input nih. Coba masukkan angka yang bener.");
            }
        }
    }

    static void TambahBarang()
    {
        Console.Write("Masukkan Nama Barang: ");
        string nama = Console.ReadLine();
        Console.Write("Harganya berapa, nih? ");
        decimal harga = decimal.Parse(Console.ReadLine());
        Console.Write("Ada Kode Barangnya nggak? ");
        string kode = Console.ReadLine();
        Console.Write("Jumlah barangnya berapa? ");
        int stock = int.Parse(Console.ReadLine());

        Barang barang = new Barang
        {
            Nama = nama,
            Harga = harga,
            Kode = kode,
            Stock = stock
        };

        daftarBarang.Add(barang);
        Console.WriteLine("Barang udah berhasil ditambahin, lho.");
    }

    static void LihatDaftarBarang()
    {
        Console.WriteLine("Ini dia Daftar Barang yang ada:");
        foreach (var barang in daftarBarang)
        {
            Console.WriteLine($"Nama: {barang.Nama}, Harga: {barang.Harga}, Kode: {barang.Kode}, Stock: {barang.Stock}");
        }
    }

    static void UpdateBarang()
    {
        Console.Write("Kode Barang yang mau di-Update apa? ");
        string kode = Console.ReadLine();

        Barang barangToUpdate = daftarBarang.Find(b => b.Kode == kode);

        if (barangToUpdate != null)
        {
            Console.Write("Harga baru barangnya berapa, ya? ");
            decimal hargaBaru = decimal.Parse(Console.ReadLine());
            Console.Write("Jumlah barangnya yang baru berapa, nih? ");
            int stockBaru = int.Parse(Console.ReadLine());

            barangToUpdate.Harga = hargaBaru;
            barangToUpdate.Stock = stockBaru;

            Console.WriteLine("Barang udah sukses di-Update, deh.");
        }
        else
        {
            Console.WriteLine("Barang dengan kode itu nggak ketemu, nih.");
        }
    }

    static void HapusBarang()
    {
        Console.Write("Kode Barang yang mau dihapus apa, ya? ");
        string kode = Console.ReadLine();

        Barang barangToRemove = daftarBarang.Find(b => b.Kode == kode);

        if (barangToRemove != null)
        {
            daftarBarang.Remove(barangToRemove);
            Console.WriteLine("Barang udah sukses dihapus, deh.");
        }
        else
        {
            Console.WriteLine("Barang dengan kode itu nggak ada, nih.");
        }
    }
}
