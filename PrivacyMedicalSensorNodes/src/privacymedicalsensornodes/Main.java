/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */

package privacymedicalsensornodes;

import javax.swing.JDialog;
import javax.swing.JFrame;
import javax.swing.JOptionPane;
import javax.swing.UIManager;

/**
 *
 * @author Elcot
 */
public class Main {
    public static void main(String[] args) 
    {        
        JFrame.setDefaultLookAndFeelDecorated(true);
        JDialog.setDefaultLookAndFeelDecorated(true);
        try
        {                    			
            UIManager.setLookAndFeel("com.jtattoo.plaf.aero.AeroLookAndFeel");                                    
            
            int snid=Integer.parseInt(JOptionPane.showInputDialog(new JFrame(),"Enter the Sensor Node id"));            
            
            SensorNodeFrame snf=new SensorNodeFrame(snid);
            snf.setTitle("Sensor Node - "+snid);
            snf.setVisible(true);
            snf.setResizable(false); 
            snf.jLabel1.setText("Sensor Node - "+snid);
            
            SensorNodeReceiver snr=new SensorNodeReceiver(snf,snid);
            snr.start();
	}
	catch (Exception ex)
	{            
            //System.out.println(ex);
	}        
    }
}
