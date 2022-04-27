# Run with `uvicorn --port 9005 main:app --reload`
import fsspec
import xarray as xr
import cf_xarray
import xpublish
from xpublish.routers import base_router, zarr_router

from edr_router import edr_router
from tree_router import tree_router

ww3 = xr.open_dataset("../datasets/ww3_72_east_coast_2022041112.nc")

gfs_mapper = fsspec.get_mapper(
    "https://ioos-code-sprint-2022.s3.amazonaws.com/gfs-wave.zarr"
)
gfs = xr.open_zarr(gfs_mapper, consolidated=True)

rest = xpublish.Rest(
    {"ww3": ww3, "gfs": gfs},
    routers=[
        base_router,
        (edr_router, {"tags": ["edr"], "prefix": "/edr"}),
        (tree_router, {"tags": ["datatree"], "prefix": "/tree"}),
        (zarr_router, {"tags": ["zarr"], "prefix": "/zarr"}),
    ],
)

app = rest.app

app.description = "Hacking on xpublish during the IOOS Code Sprint"
app.title = "IOOS xpublish"

zarr_description = """
Zarr access to NetCDF datasets.

Load by using an fsspec mapper

```python
mapper = fsspec.get_mapper("/datasets/{dataset_id}/zarr/")
ds = xr.open_zarr(mapper, consolidated=True)
```
"""

app.openapi_tags = [
    {"name": "edr", "description": "OGC Environmental Data Retrieval API"},
    {
        "name": "datatree",
        "description": "Dynamic generation of Zarr ndpyramid/Datatree for access from webmaps.",
    },
    {
        "name": "zarr",
        "description": zarr_description
        # "Zarr access to NetCDF dataset"
    },
]