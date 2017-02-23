package com.ashamis;

import javax.swing.*;
import java.awt.*;
import java.awt.image.BufferedImage;

/**
 * Created by werd on 17/02/17.
 */
public class FrmShowPic extends JPanel{
    private BufferedImage image;

    public FrmShowPic(BufferedImage img) {

        image = img;
    }

    @Override
    public void paint(Graphics g) {
        g.drawImage(image, 0, 0, this);
    }

}
