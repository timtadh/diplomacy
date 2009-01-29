import Image, ImageDraw

agg_enabled = True
try:
    import aggdraw
except:
    agg_enabled = False

def basic(landmass, path="map_temp.png"):
    im = Image.new(
        'RGBA', (landmass.width+20, landmass.height+20), color=(50,50,200,255)
    )
    if agg_enabled:
        draw = aggdraw.Draw(im)
        p = aggdraw.Pen("rgb(0,0,0)", 2.0, opacity=255)
        for terr in landmass.territories:
            for tri in terr.triangles:
                col = [int(c*255.0) for c in terr.color[0:3]]
                col_str = "rgb(%r, %r, %r)" % (col[0], col[1], col[2])
                poly = []
                b = aggdraw.Brush(col_str)
                for i in range(len(tri)/2):
                    poly.extend((
                        tri[i*2]+landmass.offset[0]+10, 
                        tri[i*2+1]+landmass.offset[1]+10
                    ))
                draw.polygon(poly, b)
            for line in terr.lines:
                draw.line((
                    line.a[0] + landmass.offset[0] + 10, 
                    line.a[1] + landmass.offset[1] + 10,
                    line.b[0] + landmass.offset[0] + 10, 
                    line.b[1] + landmass.offset[1] + 10
                ), p)
        draw.flush()
        del draw
        im.save(path, 'PNG')
        del im
        im = Image.open(path)
    else:
        draw = ImageDraw.Draw(im)
        for terr in landmass.territories:
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
                    line.a[0] + landmass.offset[0] + 10, 
                    line.a[1] + landmass.offset[1] + 10,
                    line.b[0] + landmass.offset[0] + 10, 
                    line.b[1] + landmass.offset[1] + 10
                ), fill="rgb(0, 0, 0)")
        del draw
    star = Image.open("images/star.png")
    w = star.size[0]/2
    h = star.size[1]/2
    for terr in landmass.territories:
        if terr.has_supply_center:
            x = int(terr.x + landmass.offset[0]+10)
            y = int(terr.y+landmass.offset[1]+10)
            box = (x-w, y-h, x+w, y+h)
            im.paste(star, box, star)
    im.save(path)

