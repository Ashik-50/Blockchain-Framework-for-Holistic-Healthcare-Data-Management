/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */

package privacymedicalsensornodes;

import java.net.DatagramPacket;
import java.net.DatagramSocket;
import java.util.Vector;
import javax.swing.table.DefaultTableModel;

/**
 *
 * @author Elcot
 */
public class SensorNodeReceiver extends Thread{
    
    SensorNodeFrame snf;
    int snid,port;
    
    SensorNodeReceiver(SensorNodeFrame f, int id)
    {
        snf=f;
        snid=id;
        port=snid+6000;
    }
    
    public void run()
    {
        try
        {
            DatagramSocket ds=new DatagramSocket(port);
            while(true)
            {                
                byte data[]=new byte[100000];
                DatagramPacket dp=new DatagramPacket(data,0,data.length);
                ds.receive(dp);
                String str=new String(dp.getData()).trim(); 
                System.out.println("Received: "+str);
                String req[]=str.split("#");
                if(req[0].equals("ServerDetails"))       
                {
                    DefaultTableModel dm=(DefaultTableModel)snf.jTable1.getModel();
                    Vector v=new Vector();
                    v.add(req[1].trim());
                    dm.addRow(v);
                }
                if(req[0].equals("PublicKey"))       
                {
                    snf.jTextField1.setText(req[1].trim());
                }
            }
        }
        catch(Exception e)
        {
            e.printStackTrace();
        }
    }
}
