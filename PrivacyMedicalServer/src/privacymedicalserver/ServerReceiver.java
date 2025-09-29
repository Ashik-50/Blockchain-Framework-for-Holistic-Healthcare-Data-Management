/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */

package privacymedicalserver;

import java.net.DatagramPacket;
import java.net.DatagramSocket;
import java.net.InetAddress;
import java.util.Vector;
import javax.swing.table.DefaultTableModel;

/**
 *
 * @author Elcot
 */
public class ServerReceiver extends Thread{
    
    ServerFrame sf;
    int sid,port;
    
    ServerReceiver(ServerFrame f,int id)
    {
        sf=f;
        sid=id;
        port=sid+5000;
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
                if(req[0].equals("ConnectSensor"))       
                {
                    DefaultTableModel dm=(DefaultTableModel)sf.jTable2.getModel();
                    Vector v=new Vector();
                    v.add(req[1].trim());
                    dm.addRow(v);
                }
                if(req[0].equals("Upload"))       
                {
                    DefaultTableModel dm=(DefaultTableModel)sf.jTable3.getModel();
                    Vector v=new Vector();
                    v.add(req[1].trim());
                    v.add(req[4].trim());
                    v.add(req[2].trim());
                    v.add(req[3].trim());
                    v.add(req[5].trim());  
                    v.add("-");
                    dm.addRow(v);
                }
                if(req[0].equals("pubkey"))       
                {
                    sf.jTextField1.setText(req[1].trim());
                    sf.jTextField1.setEditable(false);
                }
                if(req[0].equals("DownloadRequest"))       
                {
                    for(int i=0;i<sf.jTable3.getRowCount();i++)
                    {
                        String sensornodeid=sf.jTable3.getValueAt(i,0).toString().trim();
                        String filename=sf.jTable3.getValueAt(i,1).toString().trim();
                        String blockname=sf.jTable3.getValueAt(i,2).toString().trim();
                        String file=sf.jTable3.getValueAt(i,3).toString().trim();
                        String signature=sf.jTable3.getValueAt(i,4).toString().trim();
                        String status=sf.jTable3.getValueAt(i,5).toString().trim();
                        if(!(status.trim().equals("-")))
                        {
                            String msg="DownloadResponse#"+sensornodeid.trim()+"#"+filename.trim()+"#"+blockname.trim()+"#"+file.trim()+"#"+signature.trim();
                            int pt=4000;
                            packetTransmission(msg,pt);
                        }                
                    }
                }
            }
        }
        catch(Exception e)
        {
            e.printStackTrace();
        }
    }

    private void packetTransmission(String msg, int pt) {
        try
        {
            byte data1[]=msg.getBytes();
            DatagramSocket ds1=new DatagramSocket();
            DatagramPacket dp1=new DatagramPacket(data1,0,data1.length,InetAddress.getByName("127.0.0.1"),pt);
            ds1.send(dp1);
            System.out.println("Port is "+pt+"\n");                        
        }
        catch(Exception e)
        {
            e.printStackTrace();
        }    
    }
    
}
