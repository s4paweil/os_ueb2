package org.betriebssysteme;

public class Main {

    static int numAccounts; // Anzahl der Konten
    static int numClients; // Anzahl der Clients
    static int numTransfersPerClient; // Anzahl der Anfragen pro Client
    static String seed; // Seed zur Generierung der Zufallszahlen
    static int minStartBalance; // Minimale Startbetrag für Konten
    static int maxStartBalance; // Maximale Startbetrag für Konten
    static int minTransferAmount; // Minimaler Betrag pro Überweisung
    static int maxTransferAmount; // Maximaler Betrag pro Überweisung


    public static void main(String[] args) {
        numAccounts = 5; // Anzahl der Konten
        numClients = 10; // Anzahl der Clients
        numTransfersPerClient = 1000; // Anzahl der Anfragen pro Client
        seed = "42"; // Seed zur Generierung der Zufallszahlen
        minStartBalance = 0; // Minimale Startbetrag für Konten
        maxStartBalance = 1000; // Maximale Startbetrag für Konten
        minTransferAmount = 0; // Minimaler Betrag pro Überweisung
        maxTransferAmount = 300; // Maximaler Betrag pro Überweisung


        LCG randomSeedGenerator = new LCG(seed);

        BankServer server = new BankServer(numAccounts, randomSeedGenerator.getNextNumber(1000), minStartBalance, maxStartBalance);

        Thread serverThread = new Thread(server);
        serverThread.start();

        Thread[] clientThreads = new Thread[numClients];
        for (int i = 0; i < clientThreads.length; i++) {
            BankClient client = new BankClient(server, numTransfersPerClient, randomSeedGenerator.getNextNumber(1000), numAccounts, minTransferAmount, maxTransferAmount);
            clientThreads[i] = new Thread(client);
            clientThreads[i].start();
        }

        for (Thread clientThread : clientThreads) {
            try {
                clientThread.join();
            } catch (InterruptedException e) {
                e.printStackTrace();
            }
        }

        System.out.println(server.accountToString());
        serverThread.interrupt();
    }
}