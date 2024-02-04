import java.util.Arrays;
import java.util.logging.FileHandler;
import java.util.logging.Handler;
import java.util.logging.Logger;
import java.io.IOException;

public class BankServer extends Thread{
    private int[] accounts;
    private int[] accountsStartconfig;
    private static Logger logger = Logger.getLogger(BankServer.class.getName());

    public BankServer(int numAccounts, int seed, int minStartBalance, int maxStartBalance) {
        accounts = new int[numAccounts];
        LCG randomGenerator = new LCG(String.valueOf(seed));

        // Initialisiere Konten mit positiven Zufallswerten
        for (int i = 0; i < numAccounts; i++) {
            accounts[i] = randomGenerator.getNextNumberBetween(minStartBalance, maxStartBalance);
        }

        // Copy startconfig
        accountsStartconfig = Arrays.copyOf(accounts, accounts.length);
    }

    public synchronized void transfer(int fromAccount, int toAccount, int amount) {
        // Überprüfe, ob die Kontonummern gültig sind
        if (isValidAccount(fromAccount) && isValidAccount(toAccount)) {
            if (accounts[fromAccount - 1] >= amount) {
                accounts[fromAccount - 1] -= amount;
                accounts[toAccount - 1] += amount;
            }
        }
    }

    private boolean isValidAccount(int accountNumber) {
        return accountNumber >= 1 && accountNumber <= accounts.length;
    }

    @Override
    public void run() {
        // Der Server reagiert nur auf Anfragen der Clients, initiert jedoch keine Überweisungen
    }


    public int countTotalMoney(int[] accounts){
        int totalMoney = 0;
        for (int i = 0; i < accounts.length; i++) {
            totalMoney += accounts[i];
        }
        return totalMoney;
    }


    public String getLog(){
        String logMsg = "";

        int totalMoneyStart = countTotalMoney(accountsStartconfig);
        int totalMoneyEnd = countTotalMoney(accounts);

        if (totalMoneyStart == totalMoneyEnd) {
            logMsg += "Konten sind konsistent! Gesamtbetrag zu Beginn entspricht dem Betrag zum Ende (" + totalMoneyStart + ")\n";
        } else {
            logMsg += "Konten sind nicht konsistent! Betrag zu Beginn " + totalMoneyStart + " versus Betrag zum Ende " + totalMoneyEnd + "\n";
        }

        logMsg += String.format("%-20s%-20s%-20s\n", "Konten", "Balance start", "Balance end");
        for (int i = 0; i < accountsStartconfig.length; i++) {
            logMsg += String.format("%-20s%-20s%-20s\n", "Konto " + (i + 1), accountsStartconfig[i], accounts[i]);
        }

        return logMsg;
    }
}
