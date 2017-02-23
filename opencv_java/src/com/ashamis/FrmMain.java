package com.ashamis;

import javax.swing.*;
import java.awt.Color;
import java.awt.Graphics;
import java.awt.Image;
import java.awt.event.KeyEvent;
import java.awt.event.KeyListener;
import java.awt.image.BufferedImage;
import java.awt.image.DataBufferByte;
import java.awt.image.WritableRaster;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.awt.image.BufferedImage;

import org.opencv.core.Core;
import org.opencv.core.Mat;
import org.opencv.videoio.VideoCapture;
import org.opencv.core.CvType;
import org.opencv.core.Scalar;
import java.io.ByteArrayInputStream;
import java.io.File;
import java.io.InputStream;
import java.lang.String;

import javax.imageio.ImageIO;
import javax.swing.JFrame;
import javax.swing.JPanel;

/**
 * Created by werd on 16/02/17.
 */

public class FrmMain extends JPanel {
    static{ System.loadLibrary(Core.NATIVE_LIBRARY_NAME); }
    private JButton btnClick;
    private JPanel pnlMain;
    private JLabel lblCvVersion;
    private JTextArea textArea1;
    private JButton takePicButton;
    private BufferedImage image;

    public FrmMain() {
        btnClick.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent actionEvent) {
                System.exit(0);
            }
        });
        takePicButton.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent actionEvent) {
                TakePic();
            }
        });
    }
    public void run(){
        //FrmMain app = this;

        JFrame frm = new JFrame("LOL");
        frm.setContentPane(pnlMain);
        frm.setDefaultCloseOperation(frm.EXIT_ON_CLOSE);
        frm.pack();
        frm.setVisible(true);
        //System.out.println("Welcome to OpenCV " + Core.VERSION);
        lblCvVersion.setText("Welcome to OpenCV " + Core.VERSION);
        Mat m = new Mat(5, 10, CvType.CV_8UC1, new Scalar(0));
        //System.out.println("OpenCV Mat: " + m.dump());
        textArea1.setText("\n" + "OpenCV Mat:\n" + m.dump());
        Mat mr1 = m.row(1);
        mr1.setTo(new Scalar(1));
        textArea1.append("\n" + "TEST");
        Mat mc5 = m.col(5);
        mc5.setTo(new Scalar(5));

        textArea1.append("\n" + "OpenCV Mat data:\n" + m.dump());
        //System.out.println("OpenCV Mat data:\n" + m.dump());

        this.TakePic();
    }

    /**
     *
     */
    public void TakePic(){
        VideoCapture camera     = new VideoCapture(0);
        Mat frame               = new Mat();
        camera.read(frame);

        if(!camera.isOpened()){
            System.out.println("Error");
        }
        else {
            while(true){
                try {
                    Thread.sleep(200);
                } catch (InterruptedException e) {
                    e.printStackTrace();
                }

                if (camera.read(frame)){
                    BufferedImage image = MatToBufferedImage(frame);
                    //saveImage(image);
                    window(image, "Original Image", 0, 0);
                    window(grayscale(image), "Processed Image", 40, 60);
                    //window(loadImage("ImageName"), "Image loaded", 0, 0);
                    try {
                        Thread.sleep(1000);
                    } catch (InterruptedException e) {
                        e.printStackTrace();
                    }
                    break;
                }
            }
        }
        camera.release();
        System.out.println("Camera released");
    }


    public FrmMain(BufferedImage img) {

        image = img;
    }
    //Show image on window
    public void window(BufferedImage img, String text, int x, int y) {
        JFrame frame0 = new JFrame();

//        frame0.getContentPane().add(new FrmMain(img));
        frame0.getContentPane().add(new FrmShowPic(img));
        frame0.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        frame0.setTitle(text);
        frame0.setSize(img.getWidth(), img.getHeight() + 30);
        frame0.setLocation(x, y);
        frame0.setVisible(true);
    }
    @Override
    public void paint(Graphics g) {
        g.drawImage(image, 0, 0, this);
    }


    /**
     * Load an image
     * @param file
     * @return
     */
    public BufferedImage loadImage(String file) {
        BufferedImage img;

        try {
            File input = new File(file);
            img = ImageIO.read(input);

            return img;
        } catch (Exception e) {
            System.out.println("erro");
        }

        return null;
    }

    //Save an image
    public void saveImage(BufferedImage img) {
        try {

            File outputfile = new File("/home/werd/Images/new.png");
            ImageIO.write(img, "png", outputfile);
        } catch (Exception e) {
            System.out.println("error");
        }
    }

    /**
     * Grayscale filter
     * @param img
     * @return
     */
    public BufferedImage grayscale(BufferedImage img) {
        for (int i = 0; i < img.getHeight(); i++) {
            for (int j = 0; j < img.getWidth(); j++) {
                Color c = new Color(img.getRGB(j, i));

                int red = (int) (c.getRed() * 0.299);
                int green = (int) (c.getGreen() * 0.587);
                int blue = (int) (c.getBlue() * 0.114);

                Color newColor =
                        new Color(
                                red + green + blue,
                                red + green + blue,
                                red + green + blue);

                img.setRGB(j, i, newColor.getRGB());
            }
        }
        return img;
    }

    /**
     *
     * @param frame
     * @return
     */
    public BufferedImage MatToBufferedImage(Mat frame) {
        //Mat() to BufferedImage
        int type = 0;
        if (frame.channels() == 1) {
            type = BufferedImage.TYPE_BYTE_GRAY;
        } else if (frame.channels() == 3) {
            type = BufferedImage.TYPE_3BYTE_BGR;
        }
        BufferedImage image = new BufferedImage(frame.width(), frame.height(), type);
        WritableRaster raster = image.getRaster();
        DataBufferByte dataBuffer = (DataBufferByte) raster.getDataBuffer();
        byte[] data = dataBuffer.getData();
        frame.get(0, 0, data);

        return image;
    }

    /**
     *
     * @param args
     */
    public static void main(String[] args) {
        FrmMain app = new FrmMain();
        app.run();
    }

}
