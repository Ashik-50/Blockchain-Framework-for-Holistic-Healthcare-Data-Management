/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */

package privacymedicalserver;

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
            
            int sid=Integer.parseInt(JOptionPane.showInputDialog(new JFrame(),"Enter the Server Id"));            
            
            ServerFrame sf=new ServerFrame(sid);
            sf.setTitle("Server - "+sid);
            sf.setVisible(true);
            sf.setResizable(false); 
            sf.jLabel1.setText("Server - "+sid);
            
            ServerReceiver sr=new ServerReceiver(sf,sid);
            sr.start();
	}
	catch (Exception ex)
	{            
            //System.out.println(ex);
	}        
    }
}
