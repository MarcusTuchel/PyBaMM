#
# Bulter volmer class
#

import pybamm
from .base_kinetics import BaseKinetics


class SymmetricButlerVolmer(BaseKinetics):
    """
    Submodel which implements the symmetric forward Butler-Volmer equation:

    .. math::
        j = 2 * j_0(c) * \\sinh(ne * F * \\eta_r(c) / RT)

    Parameters
    ----------
    param : parameter class
        model parameters
    domain : str
        The domain to implement the model, either: 'Negative' or 'Positive'.
    reaction : str
        The name of the reaction being implemented
    options: dict
        A dictionary of options to be passed to the model.
        See :class:`pybamm.BaseBatteryModel`
    phase : str, optional
        Phase of the particle (default is "primary")

    **Extends:** :class:`pybamm.interface.kinetics.BaseKinetics`
    """

    def __init__(self, param, domain, reaction, options, phase="primary"):
        super().__init__(param, domain, reaction, options, phase)

    def _get_kinetics(self, j0, ne, eta_r, T, u):
        Feta_RT = self.param.F * eta_r / (self.param.R * T)
        return 2 * u * j0 * pybamm.sinh(ne * Feta_RT)

    def _get_dj_dc(self, variables):
        """See :meth:`pybamm.interface.kinetics.BaseKinetics._get_dj_dc`"""
        (
            c_e,
            delta_phi,
            j0,
            ne,
            ocp,
            T,
            u,
        ) = self._get_interface_variables_for_first_order(variables)
        eta_r = delta_phi - ocp
        Feta_RT = self.param.F * eta_r / (self.param.R * T)
        return (2 * u * j0.diff(c_e) * pybamm.sinh(ne * Feta_RT)) - (
            2 * u * j0 * prefactor * ocp.diff(c_e) * pybamm.cosh(ne * Feta_RT)
        )

    def _get_dj_ddeltaphi(self, variables):
        """See :meth:`pybamm.interface.kinetics.BaseKinetics._get_dj_ddeltaphi`"""
        _, delta_phi, j0, ne, ocp, T, u = self._get_interface_variables_for_first_order(
            variables
        )
        eta_r = delta_phi - ocp
        Feta_RT = self.param.F * eta_r / (self.param.R * T)
        return 2 * u * j0 * prefactor * pybamm.cosh(ne * Feta_RT)


class AsymmetricButlerVolmer(BaseKinetics):
    """
    Submodel which implements the asymmetric forward Butler-Volmer equation

    Parameters
    ----------
    param : parameter class
        model parameters
    domain : str
        The domain to implement the model, either: 'Negative' or 'Positive'.
    reaction : str
        The name of the reaction being implemented
    options: dict
        A dictionary of options to be passed to the model.
        See :class:`pybamm.BaseBatteryModel`
    phase : str, optional
        Phase of the particle (default is "primary")

    **Extends:** :class:`pybamm.interface.kinetics.BaseKinetics`
    """

    def __init__(self, param, domain, reaction, options, phase="primary"):
        super().__init__(param, domain, reaction, options, phase)

    def _get_kinetics(self, j0, ne, eta_r, T, u):
        alpha = self.phase_param.alpha_bv
        Feta_RT = self.param.F * eta_r / (self.param.R * T)
        arg_ox = ne * alpha * Feta_RT
        arg_red = -ne * (1 - alpha) * Feta_RT
        return u * j0 * (pybamm.exp(arg_ox) - pybamm.exp(arg_red))
