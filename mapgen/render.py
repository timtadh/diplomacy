import Image, ImageDraw, ImageFont

agg_enabled = True
try:
    import aggdraw
except:
    agg_enabled = False

def basic(landmass, path="map_temp.png", draw_cities=False):
    pad = 10
    im = Image.new(
        'RGBA', (landmass.width+pad*2, landmass.height+pad*2),
        color=(50,50,200,255)
    )
    ox = landmass.offset[0] + pad
    oy = landmass.offset[1] + pad
    if agg_enabled:
        draw = aggdraw.Draw(im)
        p = aggdraw.Pen("rgb(0,0,0)", 2.0, opacity=255)
        b_white = aggdraw.Brush("rgb(255,255,255)")
        for terr in landmass.land_terrs:
            for tri in terr.triangles:
                col = [int(c*255.0) for c in terr.color[0:3]]
                col_str = "rgb(%r, %r, %r)" % (col[0], col[1], col[2])
                poly = []
                b = aggdraw.Brush(col_str)
                for i in range(len(tri)/2):
                    poly.extend((
                        tri[i*2]+ox, 
                        tri[i*2+1]+oy
                    ))
                draw.polygon(poly, b)
            for line in terr.lines:
                draw.line((
                    line.a[0] + ox, line.a[1] + oy,
                    line.b[0] + ox, line.b[1] + oy
                ), p)
        for terr in landmass.land_terrs:
            label_rect = (
                terr.x + ox - 9, terr.y + oy + 4, 
                terr.x + ox + 9, terr.y + oy - 4
            )
            draw.rectangle(label_rect, b_white)
        for terr in landmass.sea_terrs:        
            for line in terr.lines:
                draw.line((
                    line.a[0] + ox, line.a[1] + oy,
                    line.b[0] + ox, line.b[1] + oy
                ), p)
        draw.flush()
        del draw
        im.save(path, 'PNG')
        del im
        im = Image.open(path)
    else:
        draw = ImageDraw.Draw(im)
        for terr in landmass.land_terrs:
            for tri in terr.triangles:
                col = [int(c*255.0) for c in terr.color[0:3]]
                col_str = "rgb(%r, %r, %r)" % (col[0], col[1], col[2])
                poly = []
                for i in range(len(tri)/2):
                    poly.extend((
                        tri[i*2]+landmass.offset[0]+10, 
                        tri[i*2+1]+landmass.offset[1]+10
                    ))
                draw.polygon(poly, fill=col_str)
            for line in terr.lines:
                draw.line((
                    line.a[0] + ox, line.a[1] + oy,
                    line.b[0] + ox, line.b[1] + oy
                ), fill="rgb(0, 0, 0)")
        del draw
    draw = ImageDraw.Draw(im)    
    if draw_cities:
        star = Image.open("images/star.png")
        both = Image.open("images/star_cannon.png")
        cannon = Image.open("images/cannon.png")
        anchor = Image.open("images/anchor.png")
        sw = star.size[0]/2
        sh = star.size[1]/2
        lw = both.size[0]/2
        lh = both.size[1]/2
        for terr in landmass.land_terrs:
            if terr.has_supply_center:
                if terr.occupied:
                    x = int(terr.pc_x + ox)
                    y = int(terr.pc_y + oy)
                    box = (x-lw, y-lh, x+lw, y+lh)
                    im.paste(both, box, both)
                else:
                    x = int(terr.pc_x + ox)
                    y = int(terr.pc_y + oy)
                    box = (x-sw, y-sh, x+sw, y+sh)
                    im.paste(star, box, star)
            elif terr.occupied:
                x = int(terr.pc_x + ox)
                y = int(terr.pc_y + oy)
                box = (x-sw, y-sh, x+sw, y+sh)
                if terr.is_sea:
                    im.paste(anchor, box, anchor)
                else:
                    im.paste(cannon, box, cannon)
    font = ImageFont.truetype("Inconsolata.otf", 9)
    for terr in landmass.land_terrs:
        tx = terr.x + ox - draw.textsize(terr.abbreviation)[0]/3
        ty = terr.y + oy - draw.textsize(terr.abbreviation)[1]/2
        col = "rgb(40, 40, 40)"
        draw.text((tx, ty), terr.abbreviation, fill=col, font=font)
    for terr in landmass.sea_terrs:
        tx = terr.x + ox - draw.textsize(terr.abbreviation)[0]/3
        ty = terr.y + oy - draw.textsize(terr.abbreviation)[1]/2
        col = "rgb(255,255,255)"
        draw.text((tx, ty), terr.abbreviation, fill=col, font=font)
    im.save(path)

