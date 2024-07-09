import pygmt


def plot_seafloor(da):
    """Plot seafloor age grid with PyGMT."""
    fig = pygmt.Figure()
    pygmt.makecpt(cmap="viridis", series=[0, 250], background=True)
    fig.basemap(
        region="d",
        projection="N15c",
        frame=True,
    )
    fig.grdimage(da, cmap=True, nan_transparent=True)
    fig.colorbar(frame='af+l"Sea floor age [My]"', position="+ef")
    fig.coast(shorelines=True, resolution="c", area_thresh=1e4, land="grey")
    fig.show(width=700)
