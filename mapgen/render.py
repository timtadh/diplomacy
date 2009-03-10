import Image, ImageDraw, ImageFont

agg_enabled = True
try:
    import aggdraw
except:
    agg_enabled = False

def basic(landmass, path="map_temp.png", draw_cities=False):
    pad = 80
    im = Image.new(
        'RGBA', (landmass.width+pad*2, landmass.height+pad*2),
        color=(50,50,200,255)
    )
    ox = landmass.offset[0] + pad
    oy = landmass.offset[1] + pad
    if agg_enabled:
        draw = aggdraw.Draw(im)
        p = aggdraw.Pen("rgb(0,0,0)", 2.0, opacity=255)
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
    font = ImageFont.truetype("Arial Bold.ttf", 10)
    for terr in landmass.land_terrs.union(landmass.sea_terrs):
        tx = terr.x + ox - draw.textsize(terr.abbreviation)[0]/2
        ty = terr.y + oy - draw.textsize(terr.abbreviation)[1]/2
        col = "rgb(255,255,255)"
        if hasattr(terr, 'color'):
            if terr.color[0] + terr.color[1] + terr.color[2] > 1.7:
                col = "rgb(40, 40, 40)"
        draw.text(
            (tx, ty), terr.abbreviation, fill=col, font=font
        )
    if draw_cities:
        star = Image.open("images/star.png")
        w = star.size[0]/2
        h = star.size[1]/2
        for terr in landmass.land_terrs:
            if terr.has_supply_center:
                x = int(terr.pc_x + ox)
                y = int(terr.pc_y + oy)
                box = (x-w, y-h, x+w, y+h)
                im.paste(star, box, star)
    im.save(path)

