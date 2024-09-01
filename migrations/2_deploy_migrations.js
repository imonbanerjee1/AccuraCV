const CVVerification = artifacts.require("CvVerification");

module.exports = function (deployer) {
  deployer.deploy(CVVerification);
};
