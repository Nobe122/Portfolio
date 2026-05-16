import javax.swing.*;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;

public class orderSystem {
    private JPanel root;
    private JLabel topLabel;
    private JButton BeefBowlButton;
    private JButton GarlicSproutBeefBowlButton;
    private JButton OkraBeefBowlButton;
    private JButton CheeseBeefBowlButton;
    private JButton RawEggOnBeefBowlButton;
    private JButton GrilledEelAndBeefBowlButton;
    private JButton check;
    private JLabel totalLabel;
    private JLabel orderedLabel;
    private JTextPane receivedInfo1;
    private JLabel passLabel;
    private JTextField passField;
    private JButton passButton;
    int totalPrice = 0;
    double couponrate = 1.0;

    public orderSystem() {
        BeefBowlButton.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {
                order("Beef bowl",300);
            }
        });
        BeefBowlButton.setIcon(new ImageIcon(this.getClass().getResource("01.jpg")));
        GarlicSproutBeefBowlButton.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {
                order("Garlic sprout beef bowl",400);
            }
        });
        GarlicSproutBeefBowlButton.setIcon(new ImageIcon(this.getClass().getResource("02.jpg")));
        OkraBeefBowlButton.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {
                order("Okra beef bowl",500);
            }
        });
        OkraBeefBowlButton.setIcon(new ImageIcon(this.getClass().getResource("03.jpg")));
        CheeseBeefBowlButton.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {
                order("Cheese beef bowl",600);
            }
        });
        CheeseBeefBowlButton.setIcon(new ImageIcon(this.getClass().getResource("04.jpg")));
        RawEggOnBeefBowlButton.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {
                order("Raw egg on beef bowl",350);
            }
        });
        RawEggOnBeefBowlButton.setIcon(new ImageIcon(this.getClass().getResource("05.jpg")));
        GrilledEelAndBeefBowlButton.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {
                order("Grilled eel and beef bowl",1000);
            }
        });
        GrilledEelAndBeefBowlButton.setIcon(new ImageIcon(this.getClass().getResource("06.jpg")));


        check.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {
                int confirmation = JOptionPane.showConfirmDialog(null,
                        "Would you like to checkout?",
                        "Checkout Confirmation",
                        JOptionPane.YES_NO_OPTION);
                if (confirmation==0){
                    confirmation = JOptionPane.showConfirmDialog(null,
                            "If you wanna use coupon, you have already entered the coupon?",
                            "Coupon check",
                            JOptionPane.YES_NO_OPTION);
                    if (confirmation==0){
                        JOptionPane.showMessageDialog(null,
                                "Thank you. The total price is " + (int)totalPrice*couponrate + " yen.");
                        receivedInfo1.setText("");
                        passField.setText("");
                        totalPrice = 0;
                        totalLabel.setText("Total       " + totalPrice + " yen");
                    }
                }
            }
        });
        passField.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {

            }
        });
        passButton.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {
                String couponText = passField.getText();
                if(couponrate == 0.8){
                    JOptionPane.showMessageDialog(null, "Already entered.");
                    passField.setText("");
                }
                else if(couponText.equals("0000")){
                    couponrate = 0.8;
                    JOptionPane.showMessageDialog(null,
                            "Thank you for using the coupon! It will be reflected at checkout.");
                    String currentText = receivedInfo1.getText();
                    receivedInfo1.setText(currentText + "used coupon 20%OFF!\n");
                    totalLabel.setText("Total       " + totalPrice + "(20%OFF) yen");
                }
                else{
                    JOptionPane.showMessageDialog(null,
                            "Sorry, this coupon is invalid.");
                    passField.setText("");
                }
            }
        });
    }

    public static void main(String[] args) {
        JFrame frame = new JFrame("orderSystem");
        frame.setContentPane(new orderSystem().root);
        frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        frame.pack();
        frame.setVisible(true);
    }

    void order(String food, int price){
        int confirmation = JOptionPane.showConfirmDialog(null,
                "Would you like to order " + food + "?",
                "Order Confirmation",
                JOptionPane.YES_NO_OPTION);
        if (confirmation==0){
            JOptionPane.showMessageDialog(null,
                    "Order for " + food + " received.");
            String currentText = receivedInfo1.getText();
            receivedInfo1.setText(currentText + food + "    " + price + "\n");
            totalPrice += price;
            if(couponrate == 1.0){
                totalLabel.setText("Total       " + totalPrice + " yen");
            }
            else if(couponrate == 0.8){
                totalLabel.setText("Total       " + totalPrice + "(20%OFF) yen");
            }
            else{
                JOptionPane.showMessageDialog(null,
                        "ERROR!!! Sorry, please call staff.");
            }
        }
    }
}
