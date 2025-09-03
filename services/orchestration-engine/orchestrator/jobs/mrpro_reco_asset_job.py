import mrpro
from dagster import asset, define_asset_job, AssetSelection


@asset(required_resource_keys={"datalake"}, io_manager_key="idata_io_manager")
def mrpro_direct_reconstructed_dcm(context, acquisition_results: list[dict]) -> mrpro.data.IData:
    """Reconstruct image from a list acquisition results.

    1. Loads acquisition results using the DataLakeRessource providing mrd path and meta data.
    2. Loads mrpro KData object from mrd path
    3. Performs image reconstruction using the direct reconstruction method from mrpro.
    4. Return the reconstructed IData object -> Return is passed to the idata_io_manager.
    """
    mrd_input = acquisition_results[0]["mrd_file"]
    context.log.info("Reading MRD input: %s", str(mrd_input))
    trajectory_calculator = mrpro.data.traj_calculators.KTrajectoryCartesian()
    kdata = mrpro.data.KData.from_file(mrd_input, trajectory_calculator)
    context.log.info("Loaded data: %s", kdata.shape)
    reconstruction = mrpro.algorithms.reconstruction.DirectReconstruction(kdata)
    context.log.info("Performing direct reconstruction using mrpro...")
    return reconstruction(kdata)

mrpro_direct_reconstruction_job = define_asset_job(
    name="mrpro_reconstruction_job",
    selection=AssetSelection.assets(mrpro_direct_reconstructed_dcm),
)
